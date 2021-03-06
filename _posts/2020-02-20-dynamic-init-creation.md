---
keywords: fastai
description: Dynamically create init when interfacing estimators from other packages
title: Dynamic init creation
toc: false
badges: true
comments: true
categories: [software-design]
nb_path: _notebooks/2020-02-20-dynamic-init-creation.ipynb
layout: notebook
---

<!--
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: _notebooks/2020-02-20-dynamic-init-creation.ipynb
-->

<div class="container" id="notebook-container">
        
<div class="cell border-box-sizing text_cell rendered"><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Preliminaries">Preliminaries<a class="anchor-link" href="#Preliminaries"> </a></h2>
</div>
</div>
</div>
    {% raw %}
    
<div class="cell border-box-sizing code_cell rendered">
<div class="input">

<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">!</span>pip install sktime fbprophet
</pre></div>

    </div>
</div>
</div>

</div>
    {% endraw %}

<div class="cell border-box-sizing text_cell rendered"><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Motivation">Motivation<a class="anchor-link" href="#Motivation"> </a></h2><p>The main goal of sktime is to develop a unified framework for machine
learning with time series. We do this by creating a common interface for
different types of algorithms. Instead of re-implementing algorithms from
scratch, we try to interface existing algorithm implementations whenever
possible and merely expose them through a common interface. This often
requires writing the constructor (<code>__init__.py</code>) with the appropriate
arguments from the algorithm that we want to interface.</p>
<p>In this blog post, I discuss how we can create the constructor automatically
 based on the constructor of the interfaced algorithm and any additional
 arguments we may want to add.</p>
<p>I saw the idea originally in the <a href="https://github.com/heidelbergcement/hcrystalball/blob/master/src/hcrystalball/wrappers/_base.py">HCrystalball package</a>, but cleaned up the functions a little bit to make them more
readable.</p>
<p>The idea relies on dynamic function creation, you can find a good discussion
 of that topic in this <a href="https://philip-trauner.me/blog/post/python-tips-dynamic-function-definition">blog post</a>.</p>
<h2 id="Writing-a-decorator-for-dynamic-init-creation">Writing a decorator for dynamic init creation<a class="anchor-link" href="#Writing-a-decorator-for-dynamic-init-creation"> </a></h2>
</div>
</div>
</div>
    {% raw %}
    
<div class="cell border-box-sizing code_cell rendered">
<div class="input">

<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="kn">import</span> <span class="nn">inspect</span>
<span class="kn">from</span> <span class="nn">types</span> <span class="kn">import</span> <span class="n">FunctionType</span>
<span class="kn">from</span> <span class="nn">fbprophet</span> <span class="kn">import</span> <span class="n">Prophet</span>
<span class="kn">from</span> <span class="nn">sktime.forecasting.base._base</span> <span class="kn">import</span> <span class="n">BaseForecaster</span>

<span class="k">def</span> <span class="nf">_get_param_dict</span><span class="p">(</span><span class="n">signature</span><span class="p">):</span>
    <span class="k">return</span> <span class="p">{</span>
        <span class="n">p</span><span class="o">.</span><span class="n">name</span><span class="p">:</span> <span class="n">p</span><span class="o">.</span><span class="n">default</span> <span class="k">if</span> <span class="n">p</span><span class="o">.</span><span class="n">default</span> <span class="o">!=</span> <span class="n">inspect</span><span class="o">.</span><span class="n">Parameter</span><span class="o">.</span><span class="n">empty</span> <span class="k">else</span> <span class="kc">None</span>
        <span class="k">for</span> <span class="n">p</span> <span class="ow">in</span> <span class="n">signature</span><span class="o">.</span><span class="n">parameters</span><span class="o">.</span><span class="n">values</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">p</span><span class="o">.</span><span class="n">name</span> <span class="o">!=</span> <span class="s2">&quot;self&quot;</span> <span class="ow">and</span> <span class="n">p</span><span class="o">.</span><span class="n">kind</span> <span class="o">!=</span> <span class="n">p</span><span class="o">.</span><span class="n">VAR_KEYWORD</span> <span class="ow">and</span> <span class="n">p</span><span class="o">.</span><span class="n">kind</span> <span class="o">!=</span> <span class="n">p</span><span class="o">.</span><span class="n">VAR_POSITIONAL</span>
    <span class="p">}</span>

<span class="k">def</span> <span class="nf">_get_params</span><span class="p">(</span><span class="n">func</span><span class="p">):</span>
    <span class="n">signature</span> <span class="o">=</span> <span class="n">inspect</span><span class="o">.</span><span class="n">signature</span><span class="p">(</span><span class="n">func</span><span class="p">)</span>
    <span class="k">return</span> <span class="n">_get_param_dict</span><span class="p">(</span><span class="n">signature</span><span class="p">)</span>

<span class="k">def</span> <span class="nf">create_init</span><span class="p">(</span><span class="n">model_cls</span><span class="p">):</span>
    <span class="sd">&quot;&quot;&quot;Decorator to dynamically create init function based on wrapped `model_cls`&quot;&quot;&quot;</span>

    <span class="k">def</span> <span class="nf">new_init</span><span class="p">(</span><span class="n">base_init</span><span class="p">):</span>
        <span class="c1"># combine params from wrapper class and wrapped model</span>
        <span class="n">params</span> <span class="o">=</span> <span class="n">_get_params</span><span class="p">(</span><span class="n">model_cls</span><span class="o">.</span><span class="fm">__init__</span><span class="p">)</span>
        <span class="n">params</span><span class="o">.</span><span class="n">update</span><span class="p">(</span><span class="n">_get_params</span><span class="p">(</span><span class="n">base_init</span><span class="p">))</span>

        <span class="c1"># compile function code from string representation</span>
        <span class="n">assignments</span> <span class="o">=</span> <span class="s2">&quot;; &quot;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="sa">f</span><span class="s2">&quot;self.</span><span class="si">{</span><span class="n">name</span><span class="si">}</span><span class="s2"> = </span><span class="si">{</span><span class="n">name</span><span class="si">}</span><span class="s2">&quot;</span> <span class="k">for</span> <span class="n">name</span> <span class="ow">in</span> <span class="n">params</span><span class="o">.</span><span class="n">keys</span><span class="p">()])</span>
        <span class="n">string</span> <span class="o">=</span> <span class="sa">f</span><span class="s1">&#39;def __init__(self, </span><span class="si">{</span><span class="s2">&quot;, &quot;</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">params</span><span class="o">.</span><span class="n">keys</span><span class="p">())</span><span class="si">}</span><span class="s1">): </span><span class="si">{</span><span class="n">assignments</span><span class="si">}</span><span class="s1">&#39;</span>
        <span class="n">code</span> <span class="o">=</span> <span class="nb">compile</span><span class="p">(</span><span class="n">string</span><span class="p">,</span> <span class="s2">&quot;&lt;string&gt;&quot;</span><span class="p">,</span> <span class="s2">&quot;exec&quot;</span><span class="p">)</span>

        <span class="k">return</span> <span class="n">FunctionType</span><span class="p">(</span><span class="n">code</span><span class="o">.</span><span class="n">co_consts</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="n">base_init</span><span class="o">.</span><span class="vm">__globals__</span><span class="p">,</span> <span class="n">name</span><span class="o">=</span><span class="s2">&quot;__init__&quot;</span><span class="p">,</span> <span class="n">argdefs</span><span class="o">=</span><span class="nb">tuple</span><span class="p">(</span><span class="n">params</span><span class="o">.</span><span class="n">values</span><span class="p">()))</span>

    <span class="k">return</span> <span class="n">new_init</span>
</pre></div>

    </div>
</div>
</div>

</div>
    {% endraw %}

<div class="cell border-box-sizing text_cell rendered"><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Example">Example<a class="anchor-link" href="#Example"> </a></h2><p>In this example, we use <code>fbprophet</code>.</p>

</div>
</div>
</div>
    {% raw %}
    
<div class="cell border-box-sizing code_cell rendered">
<div class="input">

<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="k">class</span> <span class="nc">ProphetForecaster</span><span class="p">(</span><span class="n">BaseForecaster</span><span class="p">):</span>
    <span class="sd">&quot;&quot;&quot;Test docstring&quot;&quot;&quot;</span>

    <span class="nd">@create_init</span><span class="p">(</span><span class="n">Prophet</span><span class="p">)</span>
    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="n">foo</span><span class="o">=</span><span class="mi">1</span><span class="p">,</span> <span class="n">bar</span><span class="o">=</span><span class="mi">2</span><span class="p">):</span>
        <span class="k">pass</span>

<span class="n">f</span> <span class="o">=</span> <span class="n">ProphetForecaster</span><span class="p">()</span>
<span class="n">f</span><span class="o">.</span><span class="n">get_params</span><span class="p">()</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">

<div class="output_area">



<div class="output_text output_subarea output_execute_result">
<pre>{&#39;bar&#39;: 2,
 &#39;changepoint_prior_scale&#39;: 0.05,
 &#39;changepoint_range&#39;: 0.8,
 &#39;changepoints&#39;: None,
 &#39;daily_seasonality&#39;: &#39;auto&#39;,
 &#39;foo&#39;: 1,
 &#39;growth&#39;: &#39;linear&#39;,
 &#39;holidays&#39;: None,
 &#39;holidays_prior_scale&#39;: 10.0,
 &#39;interval_width&#39;: 0.8,
 &#39;mcmc_samples&#39;: 0,
 &#39;n_changepoints&#39;: 25,
 &#39;seasonality_mode&#39;: &#39;additive&#39;,
 &#39;seasonality_prior_scale&#39;: 10.0,
 &#39;stan_backend&#39;: None,
 &#39;uncertainty_samples&#39;: 1000,
 &#39;weekly_seasonality&#39;: &#39;auto&#39;,
 &#39;yearly_seasonality&#39;: &#39;auto&#39;}</pre>
</div>

</div>

</div>
</div>

</div>
    {% endraw %}

<div class="cell border-box-sizing text_cell rendered"><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Future-work">Future work<a class="anchor-link" href="#Future-work"> </a></h2><p>A few further considerations:</p>
<ul>
<li>It would be preferable to use the <code>CodeType</code> <code>replace</code> method, but it's only
available from Python &gt;=3.8, see <a href="https://bugs.python.org/issue37032">https://bugs.python.org/issue37032</a></li>
<li>Ideally, we would want to add minor extensions to unify parameter names (e.g. <code>sp</code> for seasonality, <code>n_jobs</code> for multiprocessing)?</li>
<li>Can we automatically update the docstring too?</li>
</ul>

</div>
</div>
</div>
</div>
 

