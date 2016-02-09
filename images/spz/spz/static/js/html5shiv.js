



<!DOCTYPE html>
<html lang="en" class="   ">
  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# object: http://ogp.me/ns/object# article: http://ogp.me/ns/article# profile: http://ogp.me/ns/profile#">
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta http-equiv="Content-Language" content="en">
    
    
    <title>html5shiv/html5shiv.js at master · aFarkas/html5shiv · GitHub</title>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub">
    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub">
    <link rel="apple-touch-icon" sizes="57x57" href="/apple-touch-icon-114.png">
    <link rel="apple-touch-icon" sizes="114x114" href="/apple-touch-icon-114.png">
    <link rel="apple-touch-icon" sizes="72x72" href="/apple-touch-icon-144.png">
    <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144.png">
    <meta property="fb:app_id" content="1401488693436528">

      <meta content="@github" name="twitter:site" /><meta content="summary" name="twitter:card" /><meta content="aFarkas/html5shiv" name="twitter:title" /><meta content="html5shiv - This script is the defacto way to enable use of HTML5 sectioning elements in legacy Internet Explorer." name="twitter:description" /><meta content="https://avatars3.githubusercontent.com/u/188254?v=2&amp;s=400" name="twitter:image:src" />
<meta content="GitHub" property="og:site_name" /><meta content="object" property="og:type" /><meta content="https://avatars3.githubusercontent.com/u/188254?v=2&amp;s=400" property="og:image" /><meta content="aFarkas/html5shiv" property="og:title" /><meta content="https://github.com/aFarkas/html5shiv" property="og:url" /><meta content="html5shiv - This script is the defacto way to enable use of HTML5 sectioning elements in legacy Internet Explorer." property="og:description" />

    <link rel="assets" href="https://assets-cdn.github.com/">
    <link rel="conduit-xhr" href="https://ghconduit.com:25035">
    

    <meta name="msapplication-TileImage" content="/windows-tile.png">
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="selected-link" value="repo_source" data-pjax-transient>
      <meta name="google-analytics" content="UA-3769691-2">

    <meta content="collector.githubapp.com" name="octolytics-host" /><meta content="collector-cdn.github.com" name="octolytics-script-host" /><meta content="github" name="octolytics-app-id" /><meta content="2E05C580:6A42:26BEBD5:53E64206" name="octolytics-dimension-request_id" />
    

    
    
    <link rel="icon" type="image/x-icon" href="https://assets-cdn.github.com/favicon.ico">


    <meta content="authenticity_token" name="csrf-param" />
<meta content="CM2eRINcQxPFAh6GqOW3RCrJOAUk1ySfen6B+qg0XCA/37StavFdpy/4LedbRdsHYj75v3cOYgK14a6b7lyqcw==" name="csrf-token" />

    <link href="https://assets-cdn.github.com/assets/github-552c62186b3c4c8234a6c1e644620db9c279e080.css" media="all" rel="stylesheet" type="text/css" />
    <link href="https://assets-cdn.github.com/assets/github2-b855c0b37e346d3dac214385acbf7f00a78096db.css" media="all" rel="stylesheet" type="text/css" />
    


    <meta http-equiv="x-pjax-version" content="e3c046b2977f5992391282eda2c108b0">

      
  <meta name="description" content="html5shiv - This script is the defacto way to enable use of HTML5 sectioning elements in legacy Internet Explorer.">


  <meta content="188254" name="octolytics-dimension-user_id" /><meta content="aFarkas" name="octolytics-dimension-user_login" /><meta content="1358497" name="octolytics-dimension-repository_id" /><meta content="aFarkas/html5shiv" name="octolytics-dimension-repository_nwo" /><meta content="true" name="octolytics-dimension-repository_public" /><meta content="false" name="octolytics-dimension-repository_is_fork" /><meta content="1358497" name="octolytics-dimension-repository_network_root_id" /><meta content="aFarkas/html5shiv" name="octolytics-dimension-repository_network_root_nwo" />
  <link href="https://github.com/aFarkas/html5shiv/commits/master.atom" rel="alternate" title="Recent Commits to html5shiv:master" type="application/atom+xml">

  </head>


  <body class="logged_out  env-production  vis-public page-blob">
    <a href="#start-of-content" tabindex="1" class="accessibility-aid js-skip-to-content">Skip to content</a>
    <div class="wrapper">
      
      
      
      


      
      <div class="header header-logged-out">
  <div class="container clearfix">

    <a class="header-logo-wordmark" href="https://github.com/">
      <span class="mega-octicon octicon-logo-github"></span>
    </a>

    <div class="header-actions">
        <a class="button primary" href="/join">Sign up</a>
      <a class="button signin" href="/login?return_to=%2FaFarkas%2Fhtml5shiv%2Fblob%2Fmaster%2Fsrc%2Fhtml5shiv.js">Sign in</a>
    </div>

    <div class="command-bar js-command-bar  in-repository">

      <ul class="top-nav">
          <li class="explore"><a href="/explore">Explore</a></li>
          <li class="features"><a href="/features">Features</a></li>
          <li class="enterprise"><a href="https://enterprise.github.com/">Enterprise</a></li>
          <li class="blog"><a href="/blog">Blog</a></li>
      </ul>
        <form accept-charset="UTF-8" action="/search" class="command-bar-form" id="top_search_form" method="get"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /></div>

<div class="commandbar">
  <span class="message"></span>
  <input type="text" data-hotkey="s, /" name="q" id="js-command-bar-field" placeholder="Search or type a command" tabindex="1" autocapitalize="off"
    
    
    data-repo="aFarkas/html5shiv"
  >
  <div class="display hidden"></div>
</div>

    <input type="hidden" name="nwo" value="aFarkas/html5shiv">

    <div class="select-menu js-menu-container js-select-menu search-context-select-menu">
      <span class="minibutton select-menu-button js-menu-target" role="button" aria-haspopup="true">
        <span class="js-select-button">This repository</span>
      </span>

      <div class="select-menu-modal-holder js-menu-content js-navigation-container" aria-hidden="true">
        <div class="select-menu-modal">

          <div class="select-menu-item js-navigation-item js-this-repository-navigation-item selected">
            <span class="select-menu-item-icon octicon octicon-check"></span>
            <input type="radio" class="js-search-this-repository" name="search_target" value="repository" checked="checked">
            <div class="select-menu-item-text js-select-button-text">This repository</div>
          </div> <!-- /.select-menu-item -->

          <div class="select-menu-item js-navigation-item js-all-repositories-navigation-item">
            <span class="select-menu-item-icon octicon octicon-check"></span>
            <input type="radio" name="search_target" value="global">
            <div class="select-menu-item-text js-select-button-text">All repositories</div>
          </div> <!-- /.select-menu-item -->

        </div>
      </div>
    </div>

  <span class="help tooltipped tooltipped-s" aria-label="Show command bar help">
    <span class="octicon octicon-question"></span>
  </span>


  <input type="hidden" name="ref" value="cmdform">

</form>
    </div>

  </div>
</div>



      <div id="start-of-content" class="accessibility-aid"></div>
          <div class="site" itemscope itemtype="http://schema.org/WebPage">
    <div id="js-flash-container">
      
    </div>
    <div class="pagehead repohead instapaper_ignore readability-menu">
      <div class="container">
        
<ul class="pagehead-actions">


  <li>
      <a href="/login?return_to=%2FaFarkas%2Fhtml5shiv"
    class="minibutton with-count star-button tooltipped tooltipped-n"
    aria-label="You must be signed in to star a repository" rel="nofollow">
    <span class="octicon octicon-star"></span>
    Star
  </a>

    <a class="social-count js-social-count" href="/aFarkas/html5shiv/stargazers">
      4,260
    </a>

  </li>

    <li>
      <a href="/login?return_to=%2FaFarkas%2Fhtml5shiv"
        class="minibutton with-count js-toggler-target fork-button tooltipped tooltipped-n"
        aria-label="You must be signed in to fork a repository" rel="nofollow">
        <span class="octicon octicon-repo-forked"></span>
        Fork
      </a>
      <a href="/aFarkas/html5shiv/network" class="social-count">
        1,028
      </a>
    </li>
</ul>

        <h1 itemscope itemtype="http://data-vocabulary.org/Breadcrumb" class="entry-title public">
          <span class="mega-octicon octicon-repo"></span>
          <span class="author"><a href="/aFarkas" class="url fn" itemprop="url" rel="author"><span itemprop="title">aFarkas</span></a></span><!--
       --><span class="path-divider">/</span><!--
       --><strong><a href="/aFarkas/html5shiv" class="js-current-repository js-repo-home-link">html5shiv</a></strong>

          <span class="page-context-loader">
            <img alt="" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
          </span>

        </h1>
      </div><!-- /.container -->
    </div><!-- /.repohead -->

    <div class="container">
      <div class="repository-with-sidebar repo-container new-discussion-timeline  ">
        <div class="repository-sidebar clearfix">
            
<div class="sunken-menu vertical-right repo-nav js-repo-nav js-repository-container-pjax js-octicon-loaders" data-issue-count-url="/aFarkas/html5shiv/issues/counts">
  <div class="sunken-menu-contents">
    <ul class="sunken-menu-group">
      <li class="tooltipped tooltipped-w" aria-label="Code">
        <a href="/aFarkas/html5shiv" aria-label="Code" class="selected js-selected-navigation-item sunken-menu-item" data-hotkey="g c" data-pjax="true" data-selected-links="repo_source repo_downloads repo_commits repo_releases repo_tags repo_branches /aFarkas/html5shiv">
          <span class="octicon octicon-code"></span> <span class="full-word">Code</span>
          <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

        <li class="tooltipped tooltipped-w" aria-label="Issues">
          <a href="/aFarkas/html5shiv/issues" aria-label="Issues" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-hotkey="g i" data-selected-links="repo_issues repo_labels repo_milestones /aFarkas/html5shiv/issues">
            <span class="octicon octicon-issue-opened"></span> <span class="full-word">Issues</span>
            <span class="js-issue-replace-counter"></span>
            <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>        </li>

      <li class="tooltipped tooltipped-w" aria-label="Pull Requests">
        <a href="/aFarkas/html5shiv/pulls" aria-label="Pull Requests" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-hotkey="g p" data-selected-links="repo_pulls /aFarkas/html5shiv/pulls">
            <span class="octicon octicon-git-pull-request"></span> <span class="full-word">Pull Requests</span>
            <span class="js-pull-replace-counter"></span>
            <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>


        <li class="tooltipped tooltipped-w" aria-label="Wiki">
          <a href="/aFarkas/html5shiv/wiki" aria-label="Wiki" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-hotkey="g w" data-selected-links="repo_wiki /aFarkas/html5shiv/wiki">
            <span class="octicon octicon-book"></span> <span class="full-word">Wiki</span>
            <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>        </li>
    </ul>
    <div class="sunken-menu-separator"></div>
    <ul class="sunken-menu-group">

      <li class="tooltipped tooltipped-w" aria-label="Pulse">
        <a href="/aFarkas/html5shiv/pulse/weekly" aria-label="Pulse" class="js-selected-navigation-item sunken-menu-item" data-pjax="true" data-selected-links="pulse /aFarkas/html5shiv/pulse/weekly">
          <span class="octicon octicon-pulse"></span> <span class="full-word">Pulse</span>
          <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

      <li class="tooltipped tooltipped-w" aria-label="Graphs">
        <a href="/aFarkas/html5shiv/graphs" aria-label="Graphs" class="js-selected-navigation-item sunken-menu-item" data-pjax="true" data-selected-links="repo_graphs repo_contributors /aFarkas/html5shiv/graphs">
          <span class="octicon octicon-graph"></span> <span class="full-word">Graphs</span>
          <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>
    </ul>


  </div>
</div>

              <div class="only-with-full-nav">
                
  
<div class="clone-url open"
  data-protocol-type="http"
  data-url="/users/set_protocol?protocol_selector=http&amp;protocol_type=clone">
  <h3><strong>HTTPS</strong> clone URL</h3>
  <div class="input-group">
    <input type="text" class="input-mini input-monospace js-url-field"
           value="https://github.com/aFarkas/html5shiv.git" readonly="readonly">
    <span class="input-group-button">
      <button aria-label="Copy to clipboard" class="js-zeroclipboard minibutton zeroclipboard-button" data-clipboard-text="https://github.com/aFarkas/html5shiv.git" data-copied-hint="Copied!" type="button"><span class="octicon octicon-clippy"></span></button>
    </span>
  </div>
</div>

  
<div class="clone-url "
  data-protocol-type="subversion"
  data-url="/users/set_protocol?protocol_selector=subversion&amp;protocol_type=clone">
  <h3><strong>Subversion</strong> checkout URL</h3>
  <div class="input-group">
    <input type="text" class="input-mini input-monospace js-url-field"
           value="https://github.com/aFarkas/html5shiv" readonly="readonly">
    <span class="input-group-button">
      <button aria-label="Copy to clipboard" class="js-zeroclipboard minibutton zeroclipboard-button" data-clipboard-text="https://github.com/aFarkas/html5shiv" data-copied-hint="Copied!" type="button"><span class="octicon octicon-clippy"></span></button>
    </span>
  </div>
</div>


<p class="clone-options">You can clone with
      <a href="#" class="js-clone-selector" data-protocol="http">HTTPS</a>
      or <a href="#" class="js-clone-selector" data-protocol="subversion">Subversion</a>.
  <a href="https://help.github.com/articles/which-remote-url-should-i-use" class="help tooltipped tooltipped-n" aria-label="Get help on which URL is right for you.">
    <span class="octicon octicon-question"></span>
  </a>
</p>



                <a href="/aFarkas/html5shiv/archive/master.zip"
                   class="minibutton sidebar-button"
                   aria-label="Download aFarkas/html5shiv as a zip file"
                   title="Download aFarkas/html5shiv as a zip file"
                   rel="nofollow">
                  <span class="octicon octicon-cloud-download"></span>
                  Download ZIP
                </a>
              </div>
        </div><!-- /.repository-sidebar -->

        <div id="js-repo-pjax-container" class="repository-content context-loader-container" data-pjax-container>
          

<a href="/aFarkas/html5shiv/blob/dc0904b402d3c56de3e1de3cb22ede7f36430610/src/html5shiv.js" class="hidden js-permalink-shortcut" data-hotkey="y">Permalink</a>

<!-- blob contrib key: blob_contributors:v21:7518d7871e6a106cabe5bcdc068ea6f9 -->

<div class="file-navigation">
  
<div class="select-menu js-menu-container js-select-menu" >
  <span class="minibutton select-menu-button js-menu-target css-truncate" data-hotkey="w"
    data-master-branch="master"
    data-ref="master"
    title="master"
    role="button" aria-label="Switch branches or tags" tabindex="0" aria-haspopup="true">
    <span class="octicon octicon-git-branch"></span>
    <i>branch:</i>
    <span class="js-select-button css-truncate-target">master</span>
  </span>

  <div class="select-menu-modal-holder js-menu-content js-navigation-container" data-pjax aria-hidden="true">

    <div class="select-menu-modal">
      <div class="select-menu-header">
        <span class="select-menu-title">Switch branches/tags</span>
        <span class="octicon octicon-x js-menu-close" role="button" aria-label="Close"></span>
      </div> <!-- /.select-menu-header -->

      <div class="select-menu-filters">
        <div class="select-menu-text-filter">
          <input type="text" aria-label="Filter branches/tags" id="context-commitish-filter-field" class="js-filterable-field js-navigation-enable" placeholder="Filter branches/tags">
        </div>
        <div class="select-menu-tabs">
          <ul>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="branches" class="js-select-menu-tab">Branches</a>
            </li>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="tags" class="js-select-menu-tab">Tags</a>
            </li>
          </ul>
        </div><!-- /.select-menu-tabs -->
      </div><!-- /.select-menu-filters -->

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="branches">

        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/aFarkas/html5shiv/blob/defineProperty/src/html5shiv.js"
                 data-name="defineProperty"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="defineProperty">defineProperty</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/aFarkas/html5shiv/blob/gh-pages/src/html5shiv.js"
                 data-name="gh-pages"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="gh-pages">gh-pages</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/aFarkas/html5shiv/blob/iepp-htc/src/html5shiv.js"
                 data-name="iepp-htc"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="iepp-htc">iepp-htc</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/aFarkas/html5shiv/blob/innershiv/src/html5shiv.js"
                 data-name="innershiv"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="innershiv">innershiv</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item selected">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/aFarkas/html5shiv/blob/master/src/html5shiv.js"
                 data-name="master"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="master">master</a>
            </div> <!-- /.select-menu-item -->
        </div>

          <div class="select-menu-no-results">Nothing to show</div>
      </div> <!-- /.select-menu-list -->

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="tags">
        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/aFarkas/html5shiv/tree/3.7.2/src/html5shiv.js"
                 data-name="3.7.2"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="3.7.2">3.7.2</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/aFarkas/html5shiv/tree/3.7.1/src/html5shiv.js"
                 data-name="3.7.1"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="3.7.1">3.7.1</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/aFarkas/html5shiv/tree/3.7.0/src/html5shiv.js"
                 data-name="3.7.0"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="3.7.0">3.7.0</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/aFarkas/html5shiv/tree/3.6.2pre/src/html5shiv.js"
                 data-name="3.6.2pre"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="3.6.2pre">3.6.2pre</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/aFarkas/html5shiv/tree/3.6.2/src/html5shiv.js"
                 data-name="3.6.2"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="3.6.2">3.6.2</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/aFarkas/html5shiv/tree/3.6.1/src/html5shiv.js"
                 data-name="3.6.1"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="3.6.1">3.6.1</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/aFarkas/html5shiv/tree/3.6/src/html5shiv.js"
                 data-name="3.6"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="3.6">3.6</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/aFarkas/html5shiv/tree/3.5/src/html5shiv.js"
                 data-name="3.5"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="3.5">3.5</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/aFarkas/html5shiv/tree/3.4/src/html5shiv.js"
                 data-name="3.4"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="3.4">3.4</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/aFarkas/html5shiv/tree/3.3/src/html5shiv.js"
                 data-name="3.3"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="3.3">3.3</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/aFarkas/html5shiv/tree/3.2/src/html5shiv.js"
                 data-name="3.2"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="3.2">3.2</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/aFarkas/html5shiv/tree/3.1/src/html5shiv.js"
                 data-name="3.1"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="3.1">3.1</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/aFarkas/html5shiv/tree/2.2/src/html5shiv.js"
                 data-name="2.2"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="2.2">2.2</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/aFarkas/html5shiv/tree/2.1/src/html5shiv.js"
                 data-name="2.1"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="2.1">2.1</a>
            </div> <!-- /.select-menu-item -->
        </div>

        <div class="select-menu-no-results">Nothing to show</div>
      </div> <!-- /.select-menu-list -->

    </div> <!-- /.select-menu-modal -->
  </div> <!-- /.select-menu-modal-holder -->
</div> <!-- /.select-menu -->

  <div class="button-group right">
    <a href="/aFarkas/html5shiv/find/master"
          class="js-show-file-finder minibutton empty-icon tooltipped tooltipped-s"
          data-pjax
          data-hotkey="t"
          aria-label="Quickly jump between files">
      <span class="octicon octicon-list-unordered"></span>
    </a>
    <button class="js-zeroclipboard minibutton zeroclipboard-button"
          data-clipboard-text="src/html5shiv.js"
          aria-label="Copy to clipboard"
          data-copied-hint="Copied!">
      <span class="octicon octicon-clippy"></span>
    </button>
  </div>

  <div class="breadcrumb">
    <span class='repo-root js-repo-root'><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/aFarkas/html5shiv" class="" data-branch="master" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">html5shiv</span></a></span></span><span class="separator"> / </span><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/aFarkas/html5shiv/tree/master/src" class="" data-branch="master" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">src</span></a></span><span class="separator"> / </span><strong class="final-path">html5shiv.js</strong>
  </div>
</div>


  <div class="commit file-history-tease">
      <img alt="Alexander Farkas" class="main-avatar js-avatar" data-user="188254" height="24" src="https://avatars1.githubusercontent.com/u/188254?s=140" width="24" />
      <span class="author"><a href="/aFarkas" rel="author">aFarkas</a></span>
      <time datetime="2014-05-03T12:11:35+02:00" is="relative-time">May 03, 2014</time>
      <div class="commit-title">
          <a href="/aFarkas/html5shiv/commit/40df868a76f1f19ea23b123d1480d44a7195f349" class="message" data-pjax="true" title="addElements option (fixes #142)">addElements option (fixes</a> <a href="https://github.com/aFarkas/html5shiv/pull/142" class="issue-link" title="Added ability to extend the default html5shiv list of elements">#142</a><a href="/aFarkas/html5shiv/commit/40df868a76f1f19ea23b123d1480d44a7195f349" class="message" data-pjax="true" title="addElements option (fixes #142)">)</a>
      </div>

    <div class="participation">
      <p class="quickstat"><a href="#blob_contributors_box" rel="facebox"><strong>9</strong>  contributors</a></p>
          <a class="avatar tooltipped tooltipped-s" aria-label="aFarkas" href="/aFarkas/html5shiv/commits/master/src/html5shiv.js?author=aFarkas"><img alt="Alexander Farkas" class=" js-avatar" data-user="188254" height="20" src="https://avatars1.githubusercontent.com/u/188254?s=140" width="20" /></a>
    <a class="avatar tooltipped tooltipped-s" aria-label="jonathantneal" href="/aFarkas/html5shiv/commits/master/src/html5shiv.js?author=jonathantneal"><img alt="Jonathan Neal" class=" js-avatar" data-user="188426" height="20" src="https://avatars3.githubusercontent.com/u/188426?s=140" width="20" /></a>
    <a class="avatar tooltipped tooltipped-s" aria-label="jdalton" href="/aFarkas/html5shiv/commits/master/src/html5shiv.js?author=jdalton"><img alt="John-David Dalton" class=" js-avatar" data-user="4303" height="20" src="https://avatars3.githubusercontent.com/u/4303?s=140" width="20" /></a>
    <a class="avatar tooltipped tooltipped-s" aria-label="imjoshdean" href="/aFarkas/html5shiv/commits/master/src/html5shiv.js?author=imjoshdean"><img alt="Josh Dean" class=" js-avatar" data-user="252054" height="20" src="https://avatars1.githubusercontent.com/u/252054?s=140" width="20" /></a>
    <a class="avatar tooltipped tooltipped-s" aria-label="paulirish" href="/aFarkas/html5shiv/commits/master/src/html5shiv.js?author=paulirish"><img alt="Paul Irish" class=" js-avatar" data-user="39191" height="20" src="https://avatars2.githubusercontent.com/u/39191?s=140" width="20" /></a>
    <a class="avatar tooltipped tooltipped-s" aria-label="justinbmeyer" href="/aFarkas/html5shiv/commits/master/src/html5shiv.js?author=justinbmeyer"><img alt="Justin Meyer" class=" js-avatar" data-user="78602" height="20" src="https://avatars1.githubusercontent.com/u/78602?s=140" width="20" /></a>
    <a class="avatar tooltipped tooltipped-s" aria-label="mathiasbynens" href="/aFarkas/html5shiv/commits/master/src/html5shiv.js?author=mathiasbynens"><img alt="Mathias Bynens" class=" js-avatar" data-user="81942" height="20" src="https://avatars2.githubusercontent.com/u/81942?s=140" width="20" /></a>
    <a class="avatar tooltipped tooltipped-s" aria-label="nelsonmenezes" href="/aFarkas/html5shiv/commits/master/src/html5shiv.js?author=nelsonmenezes"><img alt="Nelson Menezes" class=" js-avatar" data-user="145197" height="20" src="https://avatars1.githubusercontent.com/u/145197?s=140" width="20" /></a>
    <a class="avatar tooltipped tooltipped-s" aria-label="brianblakely" href="/aFarkas/html5shiv/commits/master/src/html5shiv.js?author=brianblakely"><img alt="Brian Blakely" class=" js-avatar" data-user="401422" height="20" src="https://avatars3.githubusercontent.com/u/401422?s=140" width="20" /></a>


    </div>
    <div id="blob_contributors_box" style="display:none">
      <h2 class="facebox-header">Users who have contributed to this file</h2>
      <ul class="facebox-user-list">
          <li class="facebox-user-list-item">
            <img alt="Alexander Farkas" class=" js-avatar" data-user="188254" height="24" src="https://avatars1.githubusercontent.com/u/188254?s=140" width="24" />
            <a href="/aFarkas">aFarkas</a>
          </li>
          <li class="facebox-user-list-item">
            <img alt="Jonathan Neal" class=" js-avatar" data-user="188426" height="24" src="https://avatars3.githubusercontent.com/u/188426?s=140" width="24" />
            <a href="/jonathantneal">jonathantneal</a>
          </li>
          <li class="facebox-user-list-item">
            <img alt="John-David Dalton" class=" js-avatar" data-user="4303" height="24" src="https://avatars3.githubusercontent.com/u/4303?s=140" width="24" />
            <a href="/jdalton">jdalton</a>
          </li>
          <li class="facebox-user-list-item">
            <img alt="Josh Dean" class=" js-avatar" data-user="252054" height="24" src="https://avatars1.githubusercontent.com/u/252054?s=140" width="24" />
            <a href="/imjoshdean">imjoshdean</a>
          </li>
          <li class="facebox-user-list-item">
            <img alt="Paul Irish" class=" js-avatar" data-user="39191" height="24" src="https://avatars2.githubusercontent.com/u/39191?s=140" width="24" />
            <a href="/paulirish">paulirish</a>
          </li>
          <li class="facebox-user-list-item">
            <img alt="Justin Meyer" class=" js-avatar" data-user="78602" height="24" src="https://avatars1.githubusercontent.com/u/78602?s=140" width="24" />
            <a href="/justinbmeyer">justinbmeyer</a>
          </li>
          <li class="facebox-user-list-item">
            <img alt="Mathias Bynens" class=" js-avatar" data-user="81942" height="24" src="https://avatars2.githubusercontent.com/u/81942?s=140" width="24" />
            <a href="/mathiasbynens">mathiasbynens</a>
          </li>
          <li class="facebox-user-list-item">
            <img alt="Nelson Menezes" class=" js-avatar" data-user="145197" height="24" src="https://avatars1.githubusercontent.com/u/145197?s=140" width="24" />
            <a href="/nelsonmenezes">nelsonmenezes</a>
          </li>
          <li class="facebox-user-list-item">
            <img alt="Brian Blakely" class=" js-avatar" data-user="401422" height="24" src="https://avatars3.githubusercontent.com/u/401422?s=140" width="24" />
            <a href="/brianblakely">brianblakely</a>
          </li>
      </ul>
    </div>
  </div>

<div class="file-box">
  <div class="file">
    <div class="meta clearfix">
      <div class="info file-name">
          <span>323 lines (278 sloc)</span>
          <span class="meta-divider"></span>
        <span>10.189 kb</span>
      </div>
      <div class="actions">
        <div class="button-group">
          <a href="/aFarkas/html5shiv/raw/master/src/html5shiv.js" class="minibutton " id="raw-url">Raw</a>
            <a href="/aFarkas/html5shiv/blame/master/src/html5shiv.js" class="minibutton js-update-url-with-hash">Blame</a>
          <a href="/aFarkas/html5shiv/commits/master/src/html5shiv.js" class="minibutton " rel="nofollow">History</a>
        </div><!-- /.button-group -->


            <a class="octicon-button disabled tooltipped tooltipped-w" href="#"
               aria-label="You must be signed in to make or propose changes"><span class="octicon octicon-pencil"></span></a>

          <a class="octicon-button danger disabled tooltipped tooltipped-w" href="#"
             aria-label="You must be signed in to make or propose changes">
          <span class="octicon octicon-trashcan"></span>
        </a>
      </div><!-- /.actions -->
    </div>
      
  <div class="blob-wrapper data type-javascript">
      <table class="highlight tab-size-8 js-file-line-container">
      <tr>
        <td id="L1" class="blob-line-num js-line-number" data-line-number="1"></td>
        <td id="LC1" class="blob-line-code js-file-line"><span class="cm">/**</span></td>
      </tr>
      <tr>
        <td id="L2" class="blob-line-num js-line-number" data-line-number="2"></td>
        <td id="LC2" class="blob-line-code js-file-line"><span class="cm">* @preserve HTML5 Shiv 3.7.2 | @afarkas @jdalton @jon_neal @rem | MIT/GPL2 Licensed</span></td>
      </tr>
      <tr>
        <td id="L3" class="blob-line-num js-line-number" data-line-number="3"></td>
        <td id="LC3" class="blob-line-code js-file-line"><span class="cm">*/</span></td>
      </tr>
      <tr>
        <td id="L4" class="blob-line-num js-line-number" data-line-number="4"></td>
        <td id="LC4" class="blob-line-code js-file-line"><span class="p">;(</span><span class="kd">function</span><span class="p">(</span><span class="nb">window</span><span class="p">,</span> <span class="nb">document</span><span class="p">)</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L5" class="blob-line-num js-line-number" data-line-number="5"></td>
        <td id="LC5" class="blob-line-code js-file-line"><span class="cm">/*jshint evil:true */</span></td>
      </tr>
      <tr>
        <td id="L6" class="blob-line-num js-line-number" data-line-number="6"></td>
        <td id="LC6" class="blob-line-code js-file-line">  <span class="cm">/** version */</span></td>
      </tr>
      <tr>
        <td id="L7" class="blob-line-num js-line-number" data-line-number="7"></td>
        <td id="LC7" class="blob-line-code js-file-line">  <span class="kd">var</span> <span class="nx">version</span> <span class="o">=</span> <span class="s1">&#39;3.7.2&#39;</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L8" class="blob-line-num js-line-number" data-line-number="8"></td>
        <td id="LC8" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L9" class="blob-line-num js-line-number" data-line-number="9"></td>
        <td id="LC9" class="blob-line-code js-file-line">  <span class="cm">/** Preset options */</span></td>
      </tr>
      <tr>
        <td id="L10" class="blob-line-num js-line-number" data-line-number="10"></td>
        <td id="LC10" class="blob-line-code js-file-line">  <span class="kd">var</span> <span class="nx">options</span> <span class="o">=</span> <span class="nb">window</span><span class="p">.</span><span class="nx">html5</span> <span class="o">||</span> <span class="p">{};</span></td>
      </tr>
      <tr>
        <td id="L11" class="blob-line-num js-line-number" data-line-number="11"></td>
        <td id="LC11" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L12" class="blob-line-num js-line-number" data-line-number="12"></td>
        <td id="LC12" class="blob-line-code js-file-line">  <span class="cm">/** Used to skip problem elements */</span></td>
      </tr>
      <tr>
        <td id="L13" class="blob-line-num js-line-number" data-line-number="13"></td>
        <td id="LC13" class="blob-line-code js-file-line">  <span class="kd">var</span> <span class="nx">reSkip</span> <span class="o">=</span> <span class="sr">/^&lt;|^(?:button|map|select|textarea|object|iframe|option|optgroup)$/i</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L14" class="blob-line-num js-line-number" data-line-number="14"></td>
        <td id="LC14" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L15" class="blob-line-num js-line-number" data-line-number="15"></td>
        <td id="LC15" class="blob-line-code js-file-line">  <span class="cm">/** Not all elements can be cloned in IE **/</span></td>
      </tr>
      <tr>
        <td id="L16" class="blob-line-num js-line-number" data-line-number="16"></td>
        <td id="LC16" class="blob-line-code js-file-line">  <span class="kd">var</span> <span class="nx">saveClones</span> <span class="o">=</span> <span class="sr">/^(?:a|b|code|div|fieldset|h1|h2|h3|h4|h5|h6|i|label|li|ol|p|q|span|strong|style|table|tbody|td|th|tr|ul)$/i</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L17" class="blob-line-num js-line-number" data-line-number="17"></td>
        <td id="LC17" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L18" class="blob-line-num js-line-number" data-line-number="18"></td>
        <td id="LC18" class="blob-line-code js-file-line">  <span class="cm">/** Detect whether the browser supports default html5 styles */</span></td>
      </tr>
      <tr>
        <td id="L19" class="blob-line-num js-line-number" data-line-number="19"></td>
        <td id="LC19" class="blob-line-code js-file-line">  <span class="kd">var</span> <span class="nx">supportsHtml5Styles</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L20" class="blob-line-num js-line-number" data-line-number="20"></td>
        <td id="LC20" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L21" class="blob-line-num js-line-number" data-line-number="21"></td>
        <td id="LC21" class="blob-line-code js-file-line">  <span class="cm">/** Name of the expando, to work with multiple documents or to re-shiv one document */</span></td>
      </tr>
      <tr>
        <td id="L22" class="blob-line-num js-line-number" data-line-number="22"></td>
        <td id="LC22" class="blob-line-code js-file-line">  <span class="kd">var</span> <span class="nx">expando</span> <span class="o">=</span> <span class="s1">&#39;_html5shiv&#39;</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L23" class="blob-line-num js-line-number" data-line-number="23"></td>
        <td id="LC23" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L24" class="blob-line-num js-line-number" data-line-number="24"></td>
        <td id="LC24" class="blob-line-code js-file-line">  <span class="cm">/** The id for the the documents expando */</span></td>
      </tr>
      <tr>
        <td id="L25" class="blob-line-num js-line-number" data-line-number="25"></td>
        <td id="LC25" class="blob-line-code js-file-line">  <span class="kd">var</span> <span class="nx">expanID</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L26" class="blob-line-num js-line-number" data-line-number="26"></td>
        <td id="LC26" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L27" class="blob-line-num js-line-number" data-line-number="27"></td>
        <td id="LC27" class="blob-line-code js-file-line">  <span class="cm">/** Cached data for each document */</span></td>
      </tr>
      <tr>
        <td id="L28" class="blob-line-num js-line-number" data-line-number="28"></td>
        <td id="LC28" class="blob-line-code js-file-line">  <span class="kd">var</span> <span class="nx">expandoData</span> <span class="o">=</span> <span class="p">{};</span></td>
      </tr>
      <tr>
        <td id="L29" class="blob-line-num js-line-number" data-line-number="29"></td>
        <td id="LC29" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L30" class="blob-line-num js-line-number" data-line-number="30"></td>
        <td id="LC30" class="blob-line-code js-file-line">  <span class="cm">/** Detect whether the browser supports unknown elements */</span></td>
      </tr>
      <tr>
        <td id="L31" class="blob-line-num js-line-number" data-line-number="31"></td>
        <td id="LC31" class="blob-line-code js-file-line">  <span class="kd">var</span> <span class="nx">supportsUnknownElements</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L32" class="blob-line-num js-line-number" data-line-number="32"></td>
        <td id="LC32" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L33" class="blob-line-num js-line-number" data-line-number="33"></td>
        <td id="LC33" class="blob-line-code js-file-line">  <span class="p">(</span><span class="kd">function</span><span class="p">()</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L34" class="blob-line-num js-line-number" data-line-number="34"></td>
        <td id="LC34" class="blob-line-code js-file-line">    <span class="k">try</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L35" class="blob-line-num js-line-number" data-line-number="35"></td>
        <td id="LC35" class="blob-line-code js-file-line">        <span class="kd">var</span> <span class="nx">a</span> <span class="o">=</span> <span class="nb">document</span><span class="p">.</span><span class="nx">createElement</span><span class="p">(</span><span class="s1">&#39;a&#39;</span><span class="p">);</span></td>
      </tr>
      <tr>
        <td id="L36" class="blob-line-num js-line-number" data-line-number="36"></td>
        <td id="LC36" class="blob-line-code js-file-line">        <span class="nx">a</span><span class="p">.</span><span class="nx">innerHTML</span> <span class="o">=</span> <span class="s1">&#39;&lt;xyz&gt;&lt;/xyz&gt;&#39;</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L37" class="blob-line-num js-line-number" data-line-number="37"></td>
        <td id="LC37" class="blob-line-code js-file-line">        <span class="c1">//if the hidden property is implemented we can assume, that the browser supports basic HTML5 Styles</span></td>
      </tr>
      <tr>
        <td id="L38" class="blob-line-num js-line-number" data-line-number="38"></td>
        <td id="LC38" class="blob-line-code js-file-line">        <span class="nx">supportsHtml5Styles</span> <span class="o">=</span> <span class="p">(</span><span class="s1">&#39;hidden&#39;</span> <span class="k">in</span> <span class="nx">a</span><span class="p">);</span></td>
      </tr>
      <tr>
        <td id="L39" class="blob-line-num js-line-number" data-line-number="39"></td>
        <td id="LC39" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L40" class="blob-line-num js-line-number" data-line-number="40"></td>
        <td id="LC40" class="blob-line-code js-file-line">        <span class="nx">supportsUnknownElements</span> <span class="o">=</span> <span class="nx">a</span><span class="p">.</span><span class="nx">childNodes</span><span class="p">.</span><span class="nx">length</span> <span class="o">==</span> <span class="mi">1</span> <span class="o">||</span> <span class="p">(</span><span class="kd">function</span><span class="p">()</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L41" class="blob-line-num js-line-number" data-line-number="41"></td>
        <td id="LC41" class="blob-line-code js-file-line">          <span class="c1">// assign a false positive if unable to shiv</span></td>
      </tr>
      <tr>
        <td id="L42" class="blob-line-num js-line-number" data-line-number="42"></td>
        <td id="LC42" class="blob-line-code js-file-line">          <span class="p">(</span><span class="nb">document</span><span class="p">.</span><span class="nx">createElement</span><span class="p">)(</span><span class="s1">&#39;a&#39;</span><span class="p">);</span></td>
      </tr>
      <tr>
        <td id="L43" class="blob-line-num js-line-number" data-line-number="43"></td>
        <td id="LC43" class="blob-line-code js-file-line">          <span class="kd">var</span> <span class="nx">frag</span> <span class="o">=</span> <span class="nb">document</span><span class="p">.</span><span class="nx">createDocumentFragment</span><span class="p">();</span></td>
      </tr>
      <tr>
        <td id="L44" class="blob-line-num js-line-number" data-line-number="44"></td>
        <td id="LC44" class="blob-line-code js-file-line">          <span class="k">return</span> <span class="p">(</span></td>
      </tr>
      <tr>
        <td id="L45" class="blob-line-num js-line-number" data-line-number="45"></td>
        <td id="LC45" class="blob-line-code js-file-line">            <span class="k">typeof</span> <span class="nx">frag</span><span class="p">.</span><span class="nx">cloneNode</span> <span class="o">==</span> <span class="s1">&#39;undefined&#39;</span> <span class="o">||</span></td>
      </tr>
      <tr>
        <td id="L46" class="blob-line-num js-line-number" data-line-number="46"></td>
        <td id="LC46" class="blob-line-code js-file-line">            <span class="k">typeof</span> <span class="nx">frag</span><span class="p">.</span><span class="nx">createDocumentFragment</span> <span class="o">==</span> <span class="s1">&#39;undefined&#39;</span> <span class="o">||</span></td>
      </tr>
      <tr>
        <td id="L47" class="blob-line-num js-line-number" data-line-number="47"></td>
        <td id="LC47" class="blob-line-code js-file-line">            <span class="k">typeof</span> <span class="nx">frag</span><span class="p">.</span><span class="nx">createElement</span> <span class="o">==</span> <span class="s1">&#39;undefined&#39;</span></td>
      </tr>
      <tr>
        <td id="L48" class="blob-line-num js-line-number" data-line-number="48"></td>
        <td id="LC48" class="blob-line-code js-file-line">          <span class="p">);</span></td>
      </tr>
      <tr>
        <td id="L49" class="blob-line-num js-line-number" data-line-number="49"></td>
        <td id="LC49" class="blob-line-code js-file-line">        <span class="p">}());</span></td>
      </tr>
      <tr>
        <td id="L50" class="blob-line-num js-line-number" data-line-number="50"></td>
        <td id="LC50" class="blob-line-code js-file-line">    <span class="p">}</span> <span class="k">catch</span><span class="p">(</span><span class="nx">e</span><span class="p">)</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L51" class="blob-line-num js-line-number" data-line-number="51"></td>
        <td id="LC51" class="blob-line-code js-file-line">      <span class="c1">// assign a false positive if detection fails =&gt; unable to shiv</span></td>
      </tr>
      <tr>
        <td id="L52" class="blob-line-num js-line-number" data-line-number="52"></td>
        <td id="LC52" class="blob-line-code js-file-line">      <span class="nx">supportsHtml5Styles</span> <span class="o">=</span> <span class="kc">true</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L53" class="blob-line-num js-line-number" data-line-number="53"></td>
        <td id="LC53" class="blob-line-code js-file-line">      <span class="nx">supportsUnknownElements</span> <span class="o">=</span> <span class="kc">true</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L54" class="blob-line-num js-line-number" data-line-number="54"></td>
        <td id="LC54" class="blob-line-code js-file-line">    <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L55" class="blob-line-num js-line-number" data-line-number="55"></td>
        <td id="LC55" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L56" class="blob-line-num js-line-number" data-line-number="56"></td>
        <td id="LC56" class="blob-line-code js-file-line">  <span class="p">}());</span></td>
      </tr>
      <tr>
        <td id="L57" class="blob-line-num js-line-number" data-line-number="57"></td>
        <td id="LC57" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L58" class="blob-line-num js-line-number" data-line-number="58"></td>
        <td id="LC58" class="blob-line-code js-file-line">  <span class="cm">/*--------------------------------------------------------------------------*/</span></td>
      </tr>
      <tr>
        <td id="L59" class="blob-line-num js-line-number" data-line-number="59"></td>
        <td id="LC59" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L60" class="blob-line-num js-line-number" data-line-number="60"></td>
        <td id="LC60" class="blob-line-code js-file-line">  <span class="cm">/**</span></td>
      </tr>
      <tr>
        <td id="L61" class="blob-line-num js-line-number" data-line-number="61"></td>
        <td id="LC61" class="blob-line-code js-file-line"><span class="cm">   * Creates a style sheet with the given CSS text and adds it to the document.</span></td>
      </tr>
      <tr>
        <td id="L62" class="blob-line-num js-line-number" data-line-number="62"></td>
        <td id="LC62" class="blob-line-code js-file-line"><span class="cm">   * @private</span></td>
      </tr>
      <tr>
        <td id="L63" class="blob-line-num js-line-number" data-line-number="63"></td>
        <td id="LC63" class="blob-line-code js-file-line"><span class="cm">   * @param {Document} ownerDocument The document.</span></td>
      </tr>
      <tr>
        <td id="L64" class="blob-line-num js-line-number" data-line-number="64"></td>
        <td id="LC64" class="blob-line-code js-file-line"><span class="cm">   * @param {String} cssText The CSS text.</span></td>
      </tr>
      <tr>
        <td id="L65" class="blob-line-num js-line-number" data-line-number="65"></td>
        <td id="LC65" class="blob-line-code js-file-line"><span class="cm">   * @returns {StyleSheet} The style element.</span></td>
      </tr>
      <tr>
        <td id="L66" class="blob-line-num js-line-number" data-line-number="66"></td>
        <td id="LC66" class="blob-line-code js-file-line"><span class="cm">   */</span></td>
      </tr>
      <tr>
        <td id="L67" class="blob-line-num js-line-number" data-line-number="67"></td>
        <td id="LC67" class="blob-line-code js-file-line">  <span class="kd">function</span> <span class="nx">addStyleSheet</span><span class="p">(</span><span class="nx">ownerDocument</span><span class="p">,</span> <span class="nx">cssText</span><span class="p">)</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L68" class="blob-line-num js-line-number" data-line-number="68"></td>
        <td id="LC68" class="blob-line-code js-file-line">    <span class="kd">var</span> <span class="nx">p</span> <span class="o">=</span> <span class="nx">ownerDocument</span><span class="p">.</span><span class="nx">createElement</span><span class="p">(</span><span class="s1">&#39;p&#39;</span><span class="p">),</span></td>
      </tr>
      <tr>
        <td id="L69" class="blob-line-num js-line-number" data-line-number="69"></td>
        <td id="LC69" class="blob-line-code js-file-line">        <span class="nx">parent</span> <span class="o">=</span> <span class="nx">ownerDocument</span><span class="p">.</span><span class="nx">getElementsByTagName</span><span class="p">(</span><span class="s1">&#39;head&#39;</span><span class="p">)[</span><span class="mi">0</span><span class="p">]</span> <span class="o">||</span> <span class="nx">ownerDocument</span><span class="p">.</span><span class="nx">documentElement</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L70" class="blob-line-num js-line-number" data-line-number="70"></td>
        <td id="LC70" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L71" class="blob-line-num js-line-number" data-line-number="71"></td>
        <td id="LC71" class="blob-line-code js-file-line">    <span class="nx">p</span><span class="p">.</span><span class="nx">innerHTML</span> <span class="o">=</span> <span class="s1">&#39;x&lt;style&gt;&#39;</span> <span class="o">+</span> <span class="nx">cssText</span> <span class="o">+</span> <span class="s1">&#39;&lt;/style&gt;&#39;</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L72" class="blob-line-num js-line-number" data-line-number="72"></td>
        <td id="LC72" class="blob-line-code js-file-line">    <span class="k">return</span> <span class="nx">parent</span><span class="p">.</span><span class="nx">insertBefore</span><span class="p">(</span><span class="nx">p</span><span class="p">.</span><span class="nx">lastChild</span><span class="p">,</span> <span class="nx">parent</span><span class="p">.</span><span class="nx">firstChild</span><span class="p">);</span></td>
      </tr>
      <tr>
        <td id="L73" class="blob-line-num js-line-number" data-line-number="73"></td>
        <td id="LC73" class="blob-line-code js-file-line">  <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L74" class="blob-line-num js-line-number" data-line-number="74"></td>
        <td id="LC74" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L75" class="blob-line-num js-line-number" data-line-number="75"></td>
        <td id="LC75" class="blob-line-code js-file-line">  <span class="cm">/**</span></td>
      </tr>
      <tr>
        <td id="L76" class="blob-line-num js-line-number" data-line-number="76"></td>
        <td id="LC76" class="blob-line-code js-file-line"><span class="cm">   * Returns the value of `html5.elements` as an array.</span></td>
      </tr>
      <tr>
        <td id="L77" class="blob-line-num js-line-number" data-line-number="77"></td>
        <td id="LC77" class="blob-line-code js-file-line"><span class="cm">   * @private</span></td>
      </tr>
      <tr>
        <td id="L78" class="blob-line-num js-line-number" data-line-number="78"></td>
        <td id="LC78" class="blob-line-code js-file-line"><span class="cm">   * @returns {Array} An array of shived element node names.</span></td>
      </tr>
      <tr>
        <td id="L79" class="blob-line-num js-line-number" data-line-number="79"></td>
        <td id="LC79" class="blob-line-code js-file-line"><span class="cm">   */</span></td>
      </tr>
      <tr>
        <td id="L80" class="blob-line-num js-line-number" data-line-number="80"></td>
        <td id="LC80" class="blob-line-code js-file-line">  <span class="kd">function</span> <span class="nx">getElements</span><span class="p">()</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L81" class="blob-line-num js-line-number" data-line-number="81"></td>
        <td id="LC81" class="blob-line-code js-file-line">    <span class="kd">var</span> <span class="nx">elements</span> <span class="o">=</span> <span class="nx">html5</span><span class="p">.</span><span class="nx">elements</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L82" class="blob-line-num js-line-number" data-line-number="82"></td>
        <td id="LC82" class="blob-line-code js-file-line">    <span class="k">return</span> <span class="k">typeof</span> <span class="nx">elements</span> <span class="o">==</span> <span class="s1">&#39;string&#39;</span> <span class="o">?</span> <span class="nx">elements</span><span class="p">.</span><span class="nx">split</span><span class="p">(</span><span class="s1">&#39; &#39;</span><span class="p">)</span> <span class="o">:</span> <span class="nx">elements</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L83" class="blob-line-num js-line-number" data-line-number="83"></td>
        <td id="LC83" class="blob-line-code js-file-line">  <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L84" class="blob-line-num js-line-number" data-line-number="84"></td>
        <td id="LC84" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L85" class="blob-line-num js-line-number" data-line-number="85"></td>
        <td id="LC85" class="blob-line-code js-file-line">  <span class="cm">/**</span></td>
      </tr>
      <tr>
        <td id="L86" class="blob-line-num js-line-number" data-line-number="86"></td>
        <td id="LC86" class="blob-line-code js-file-line"><span class="cm">   * Extends the built-in list of html5 elements</span></td>
      </tr>
      <tr>
        <td id="L87" class="blob-line-num js-line-number" data-line-number="87"></td>
        <td id="LC87" class="blob-line-code js-file-line"><span class="cm">   * @memberOf html5</span></td>
      </tr>
      <tr>
        <td id="L88" class="blob-line-num js-line-number" data-line-number="88"></td>
        <td id="LC88" class="blob-line-code js-file-line"><span class="cm">   * @param {String|Array} newElements whitespace separated list or array of new element names to shiv</span></td>
      </tr>
      <tr>
        <td id="L89" class="blob-line-num js-line-number" data-line-number="89"></td>
        <td id="LC89" class="blob-line-code js-file-line"><span class="cm">   * @param {Document} ownerDocument The context document.</span></td>
      </tr>
      <tr>
        <td id="L90" class="blob-line-num js-line-number" data-line-number="90"></td>
        <td id="LC90" class="blob-line-code js-file-line"><span class="cm">   */</span></td>
      </tr>
      <tr>
        <td id="L91" class="blob-line-num js-line-number" data-line-number="91"></td>
        <td id="LC91" class="blob-line-code js-file-line">  <span class="kd">function</span> <span class="nx">addElements</span><span class="p">(</span><span class="nx">newElements</span><span class="p">,</span> <span class="nx">ownerDocument</span><span class="p">)</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L92" class="blob-line-num js-line-number" data-line-number="92"></td>
        <td id="LC92" class="blob-line-code js-file-line">    <span class="kd">var</span> <span class="nx">elements</span> <span class="o">=</span> <span class="nx">html5</span><span class="p">.</span><span class="nx">elements</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L93" class="blob-line-num js-line-number" data-line-number="93"></td>
        <td id="LC93" class="blob-line-code js-file-line">    <span class="k">if</span><span class="p">(</span><span class="k">typeof</span> <span class="nx">elements</span> <span class="o">!=</span> <span class="s1">&#39;string&#39;</span><span class="p">){</span></td>
      </tr>
      <tr>
        <td id="L94" class="blob-line-num js-line-number" data-line-number="94"></td>
        <td id="LC94" class="blob-line-code js-file-line">      <span class="nx">elements</span> <span class="o">=</span> <span class="nx">elements</span><span class="p">.</span><span class="nx">join</span><span class="p">(</span><span class="s1">&#39; &#39;</span><span class="p">);</span></td>
      </tr>
      <tr>
        <td id="L95" class="blob-line-num js-line-number" data-line-number="95"></td>
        <td id="LC95" class="blob-line-code js-file-line">    <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L96" class="blob-line-num js-line-number" data-line-number="96"></td>
        <td id="LC96" class="blob-line-code js-file-line">    <span class="k">if</span><span class="p">(</span><span class="k">typeof</span> <span class="nx">newElements</span> <span class="o">!=</span> <span class="s1">&#39;string&#39;</span><span class="p">){</span></td>
      </tr>
      <tr>
        <td id="L97" class="blob-line-num js-line-number" data-line-number="97"></td>
        <td id="LC97" class="blob-line-code js-file-line">      <span class="nx">newElements</span> <span class="o">=</span> <span class="nx">newElements</span><span class="p">.</span><span class="nx">join</span><span class="p">(</span><span class="s1">&#39; &#39;</span><span class="p">);</span></td>
      </tr>
      <tr>
        <td id="L98" class="blob-line-num js-line-number" data-line-number="98"></td>
        <td id="LC98" class="blob-line-code js-file-line">    <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L99" class="blob-line-num js-line-number" data-line-number="99"></td>
        <td id="LC99" class="blob-line-code js-file-line">    <span class="nx">html5</span><span class="p">.</span><span class="nx">elements</span> <span class="o">=</span> <span class="nx">elements</span> <span class="o">+</span><span class="s1">&#39; &#39;</span><span class="o">+</span> <span class="nx">newElements</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L100" class="blob-line-num js-line-number" data-line-number="100"></td>
        <td id="LC100" class="blob-line-code js-file-line">    <span class="nx">shivDocument</span><span class="p">(</span><span class="nx">ownerDocument</span><span class="p">);</span></td>
      </tr>
      <tr>
        <td id="L101" class="blob-line-num js-line-number" data-line-number="101"></td>
        <td id="LC101" class="blob-line-code js-file-line">  <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L102" class="blob-line-num js-line-number" data-line-number="102"></td>
        <td id="LC102" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L103" class="blob-line-num js-line-number" data-line-number="103"></td>
        <td id="LC103" class="blob-line-code js-file-line">   <span class="cm">/**</span></td>
      </tr>
      <tr>
        <td id="L104" class="blob-line-num js-line-number" data-line-number="104"></td>
        <td id="LC104" class="blob-line-code js-file-line"><span class="cm">   * Returns the data associated to the given document</span></td>
      </tr>
      <tr>
        <td id="L105" class="blob-line-num js-line-number" data-line-number="105"></td>
        <td id="LC105" class="blob-line-code js-file-line"><span class="cm">   * @private</span></td>
      </tr>
      <tr>
        <td id="L106" class="blob-line-num js-line-number" data-line-number="106"></td>
        <td id="LC106" class="blob-line-code js-file-line"><span class="cm">   * @param {Document} ownerDocument The document.</span></td>
      </tr>
      <tr>
        <td id="L107" class="blob-line-num js-line-number" data-line-number="107"></td>
        <td id="LC107" class="blob-line-code js-file-line"><span class="cm">   * @returns {Object} An object of data.</span></td>
      </tr>
      <tr>
        <td id="L108" class="blob-line-num js-line-number" data-line-number="108"></td>
        <td id="LC108" class="blob-line-code js-file-line"><span class="cm">   */</span></td>
      </tr>
      <tr>
        <td id="L109" class="blob-line-num js-line-number" data-line-number="109"></td>
        <td id="LC109" class="blob-line-code js-file-line">  <span class="kd">function</span> <span class="nx">getExpandoData</span><span class="p">(</span><span class="nx">ownerDocument</span><span class="p">)</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L110" class="blob-line-num js-line-number" data-line-number="110"></td>
        <td id="LC110" class="blob-line-code js-file-line">    <span class="kd">var</span> <span class="nx">data</span> <span class="o">=</span> <span class="nx">expandoData</span><span class="p">[</span><span class="nx">ownerDocument</span><span class="p">[</span><span class="nx">expando</span><span class="p">]];</span></td>
      </tr>
      <tr>
        <td id="L111" class="blob-line-num js-line-number" data-line-number="111"></td>
        <td id="LC111" class="blob-line-code js-file-line">    <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="nx">data</span><span class="p">)</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L112" class="blob-line-num js-line-number" data-line-number="112"></td>
        <td id="LC112" class="blob-line-code js-file-line">        <span class="nx">data</span> <span class="o">=</span> <span class="p">{};</span></td>
      </tr>
      <tr>
        <td id="L113" class="blob-line-num js-line-number" data-line-number="113"></td>
        <td id="LC113" class="blob-line-code js-file-line">        <span class="nx">expanID</span><span class="o">++</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L114" class="blob-line-num js-line-number" data-line-number="114"></td>
        <td id="LC114" class="blob-line-code js-file-line">        <span class="nx">ownerDocument</span><span class="p">[</span><span class="nx">expando</span><span class="p">]</span> <span class="o">=</span> <span class="nx">expanID</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L115" class="blob-line-num js-line-number" data-line-number="115"></td>
        <td id="LC115" class="blob-line-code js-file-line">        <span class="nx">expandoData</span><span class="p">[</span><span class="nx">expanID</span><span class="p">]</span> <span class="o">=</span> <span class="nx">data</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L116" class="blob-line-num js-line-number" data-line-number="116"></td>
        <td id="LC116" class="blob-line-code js-file-line">    <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L117" class="blob-line-num js-line-number" data-line-number="117"></td>
        <td id="LC117" class="blob-line-code js-file-line">    <span class="k">return</span> <span class="nx">data</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L118" class="blob-line-num js-line-number" data-line-number="118"></td>
        <td id="LC118" class="blob-line-code js-file-line">  <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L119" class="blob-line-num js-line-number" data-line-number="119"></td>
        <td id="LC119" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L120" class="blob-line-num js-line-number" data-line-number="120"></td>
        <td id="LC120" class="blob-line-code js-file-line">  <span class="cm">/**</span></td>
      </tr>
      <tr>
        <td id="L121" class="blob-line-num js-line-number" data-line-number="121"></td>
        <td id="LC121" class="blob-line-code js-file-line"><span class="cm">   * returns a shived element for the given nodeName and document</span></td>
      </tr>
      <tr>
        <td id="L122" class="blob-line-num js-line-number" data-line-number="122"></td>
        <td id="LC122" class="blob-line-code js-file-line"><span class="cm">   * @memberOf html5</span></td>
      </tr>
      <tr>
        <td id="L123" class="blob-line-num js-line-number" data-line-number="123"></td>
        <td id="LC123" class="blob-line-code js-file-line"><span class="cm">   * @param {String} nodeName name of the element</span></td>
      </tr>
      <tr>
        <td id="L124" class="blob-line-num js-line-number" data-line-number="124"></td>
        <td id="LC124" class="blob-line-code js-file-line"><span class="cm">   * @param {Document} ownerDocument The context document.</span></td>
      </tr>
      <tr>
        <td id="L125" class="blob-line-num js-line-number" data-line-number="125"></td>
        <td id="LC125" class="blob-line-code js-file-line"><span class="cm">   * @returns {Object} The shived element.</span></td>
      </tr>
      <tr>
        <td id="L126" class="blob-line-num js-line-number" data-line-number="126"></td>
        <td id="LC126" class="blob-line-code js-file-line"><span class="cm">   */</span></td>
      </tr>
      <tr>
        <td id="L127" class="blob-line-num js-line-number" data-line-number="127"></td>
        <td id="LC127" class="blob-line-code js-file-line">  <span class="kd">function</span> <span class="nx">createElement</span><span class="p">(</span><span class="nx">nodeName</span><span class="p">,</span> <span class="nx">ownerDocument</span><span class="p">,</span> <span class="nx">data</span><span class="p">){</span></td>
      </tr>
      <tr>
        <td id="L128" class="blob-line-num js-line-number" data-line-number="128"></td>
        <td id="LC128" class="blob-line-code js-file-line">    <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="nx">ownerDocument</span><span class="p">)</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L129" class="blob-line-num js-line-number" data-line-number="129"></td>
        <td id="LC129" class="blob-line-code js-file-line">        <span class="nx">ownerDocument</span> <span class="o">=</span> <span class="nb">document</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L130" class="blob-line-num js-line-number" data-line-number="130"></td>
        <td id="LC130" class="blob-line-code js-file-line">    <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L131" class="blob-line-num js-line-number" data-line-number="131"></td>
        <td id="LC131" class="blob-line-code js-file-line">    <span class="k">if</span><span class="p">(</span><span class="nx">supportsUnknownElements</span><span class="p">){</span></td>
      </tr>
      <tr>
        <td id="L132" class="blob-line-num js-line-number" data-line-number="132"></td>
        <td id="LC132" class="blob-line-code js-file-line">        <span class="k">return</span> <span class="nx">ownerDocument</span><span class="p">.</span><span class="nx">createElement</span><span class="p">(</span><span class="nx">nodeName</span><span class="p">);</span></td>
      </tr>
      <tr>
        <td id="L133" class="blob-line-num js-line-number" data-line-number="133"></td>
        <td id="LC133" class="blob-line-code js-file-line">    <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L134" class="blob-line-num js-line-number" data-line-number="134"></td>
        <td id="LC134" class="blob-line-code js-file-line">    <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="nx">data</span><span class="p">)</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L135" class="blob-line-num js-line-number" data-line-number="135"></td>
        <td id="LC135" class="blob-line-code js-file-line">        <span class="nx">data</span> <span class="o">=</span> <span class="nx">getExpandoData</span><span class="p">(</span><span class="nx">ownerDocument</span><span class="p">);</span></td>
      </tr>
      <tr>
        <td id="L136" class="blob-line-num js-line-number" data-line-number="136"></td>
        <td id="LC136" class="blob-line-code js-file-line">    <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L137" class="blob-line-num js-line-number" data-line-number="137"></td>
        <td id="LC137" class="blob-line-code js-file-line">    <span class="kd">var</span> <span class="nx">node</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L138" class="blob-line-num js-line-number" data-line-number="138"></td>
        <td id="LC138" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L139" class="blob-line-num js-line-number" data-line-number="139"></td>
        <td id="LC139" class="blob-line-code js-file-line">    <span class="k">if</span> <span class="p">(</span><span class="nx">data</span><span class="p">.</span><span class="nx">cache</span><span class="p">[</span><span class="nx">nodeName</span><span class="p">])</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L140" class="blob-line-num js-line-number" data-line-number="140"></td>
        <td id="LC140" class="blob-line-code js-file-line">        <span class="nx">node</span> <span class="o">=</span> <span class="nx">data</span><span class="p">.</span><span class="nx">cache</span><span class="p">[</span><span class="nx">nodeName</span><span class="p">].</span><span class="nx">cloneNode</span><span class="p">();</span></td>
      </tr>
      <tr>
        <td id="L141" class="blob-line-num js-line-number" data-line-number="141"></td>
        <td id="LC141" class="blob-line-code js-file-line">    <span class="p">}</span> <span class="k">else</span> <span class="k">if</span> <span class="p">(</span><span class="nx">saveClones</span><span class="p">.</span><span class="nx">test</span><span class="p">(</span><span class="nx">nodeName</span><span class="p">))</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L142" class="blob-line-num js-line-number" data-line-number="142"></td>
        <td id="LC142" class="blob-line-code js-file-line">        <span class="nx">node</span> <span class="o">=</span> <span class="p">(</span><span class="nx">data</span><span class="p">.</span><span class="nx">cache</span><span class="p">[</span><span class="nx">nodeName</span><span class="p">]</span> <span class="o">=</span> <span class="nx">data</span><span class="p">.</span><span class="nx">createElem</span><span class="p">(</span><span class="nx">nodeName</span><span class="p">)).</span><span class="nx">cloneNode</span><span class="p">();</span></td>
      </tr>
      <tr>
        <td id="L143" class="blob-line-num js-line-number" data-line-number="143"></td>
        <td id="LC143" class="blob-line-code js-file-line">    <span class="p">}</span> <span class="k">else</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L144" class="blob-line-num js-line-number" data-line-number="144"></td>
        <td id="LC144" class="blob-line-code js-file-line">        <span class="nx">node</span> <span class="o">=</span> <span class="nx">data</span><span class="p">.</span><span class="nx">createElem</span><span class="p">(</span><span class="nx">nodeName</span><span class="p">);</span></td>
      </tr>
      <tr>
        <td id="L145" class="blob-line-num js-line-number" data-line-number="145"></td>
        <td id="LC145" class="blob-line-code js-file-line">    <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L146" class="blob-line-num js-line-number" data-line-number="146"></td>
        <td id="LC146" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L147" class="blob-line-num js-line-number" data-line-number="147"></td>
        <td id="LC147" class="blob-line-code js-file-line">    <span class="c1">// Avoid adding some elements to fragments in IE &lt; 9 because</span></td>
      </tr>
      <tr>
        <td id="L148" class="blob-line-num js-line-number" data-line-number="148"></td>
        <td id="LC148" class="blob-line-code js-file-line">    <span class="c1">// * Attributes like `name` or `type` cannot be set/changed once an element</span></td>
      </tr>
      <tr>
        <td id="L149" class="blob-line-num js-line-number" data-line-number="149"></td>
        <td id="LC149" class="blob-line-code js-file-line">    <span class="c1">//   is inserted into a document/fragment</span></td>
      </tr>
      <tr>
        <td id="L150" class="blob-line-num js-line-number" data-line-number="150"></td>
        <td id="LC150" class="blob-line-code js-file-line">    <span class="c1">// * Link elements with `src` attributes that are inaccessible, as with</span></td>
      </tr>
      <tr>
        <td id="L151" class="blob-line-num js-line-number" data-line-number="151"></td>
        <td id="LC151" class="blob-line-code js-file-line">    <span class="c1">//   a 403 response, will cause the tab/window to crash</span></td>
      </tr>
      <tr>
        <td id="L152" class="blob-line-num js-line-number" data-line-number="152"></td>
        <td id="LC152" class="blob-line-code js-file-line">    <span class="c1">// * Script elements appended to fragments will execute when their `src`</span></td>
      </tr>
      <tr>
        <td id="L153" class="blob-line-num js-line-number" data-line-number="153"></td>
        <td id="LC153" class="blob-line-code js-file-line">    <span class="c1">//   or `text` property is set</span></td>
      </tr>
      <tr>
        <td id="L154" class="blob-line-num js-line-number" data-line-number="154"></td>
        <td id="LC154" class="blob-line-code js-file-line">    <span class="k">return</span> <span class="nx">node</span><span class="p">.</span><span class="nx">canHaveChildren</span> <span class="o">&amp;&amp;</span> <span class="o">!</span><span class="nx">reSkip</span><span class="p">.</span><span class="nx">test</span><span class="p">(</span><span class="nx">nodeName</span><span class="p">)</span> <span class="o">&amp;&amp;</span> <span class="o">!</span><span class="nx">node</span><span class="p">.</span><span class="nx">tagUrn</span> <span class="o">?</span> <span class="nx">data</span><span class="p">.</span><span class="nx">frag</span><span class="p">.</span><span class="nx">appendChild</span><span class="p">(</span><span class="nx">node</span><span class="p">)</span> <span class="o">:</span> <span class="nx">node</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L155" class="blob-line-num js-line-number" data-line-number="155"></td>
        <td id="LC155" class="blob-line-code js-file-line">  <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L156" class="blob-line-num js-line-number" data-line-number="156"></td>
        <td id="LC156" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L157" class="blob-line-num js-line-number" data-line-number="157"></td>
        <td id="LC157" class="blob-line-code js-file-line">  <span class="cm">/**</span></td>
      </tr>
      <tr>
        <td id="L158" class="blob-line-num js-line-number" data-line-number="158"></td>
        <td id="LC158" class="blob-line-code js-file-line"><span class="cm">   * returns a shived DocumentFragment for the given document</span></td>
      </tr>
      <tr>
        <td id="L159" class="blob-line-num js-line-number" data-line-number="159"></td>
        <td id="LC159" class="blob-line-code js-file-line"><span class="cm">   * @memberOf html5</span></td>
      </tr>
      <tr>
        <td id="L160" class="blob-line-num js-line-number" data-line-number="160"></td>
        <td id="LC160" class="blob-line-code js-file-line"><span class="cm">   * @param {Document} ownerDocument The context document.</span></td>
      </tr>
      <tr>
        <td id="L161" class="blob-line-num js-line-number" data-line-number="161"></td>
        <td id="LC161" class="blob-line-code js-file-line"><span class="cm">   * @returns {Object} The shived DocumentFragment.</span></td>
      </tr>
      <tr>
        <td id="L162" class="blob-line-num js-line-number" data-line-number="162"></td>
        <td id="LC162" class="blob-line-code js-file-line"><span class="cm">   */</span></td>
      </tr>
      <tr>
        <td id="L163" class="blob-line-num js-line-number" data-line-number="163"></td>
        <td id="LC163" class="blob-line-code js-file-line">  <span class="kd">function</span> <span class="nx">createDocumentFragment</span><span class="p">(</span><span class="nx">ownerDocument</span><span class="p">,</span> <span class="nx">data</span><span class="p">){</span></td>
      </tr>
      <tr>
        <td id="L164" class="blob-line-num js-line-number" data-line-number="164"></td>
        <td id="LC164" class="blob-line-code js-file-line">    <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="nx">ownerDocument</span><span class="p">)</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L165" class="blob-line-num js-line-number" data-line-number="165"></td>
        <td id="LC165" class="blob-line-code js-file-line">        <span class="nx">ownerDocument</span> <span class="o">=</span> <span class="nb">document</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L166" class="blob-line-num js-line-number" data-line-number="166"></td>
        <td id="LC166" class="blob-line-code js-file-line">    <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L167" class="blob-line-num js-line-number" data-line-number="167"></td>
        <td id="LC167" class="blob-line-code js-file-line">    <span class="k">if</span><span class="p">(</span><span class="nx">supportsUnknownElements</span><span class="p">){</span></td>
      </tr>
      <tr>
        <td id="L168" class="blob-line-num js-line-number" data-line-number="168"></td>
        <td id="LC168" class="blob-line-code js-file-line">        <span class="k">return</span> <span class="nx">ownerDocument</span><span class="p">.</span><span class="nx">createDocumentFragment</span><span class="p">();</span></td>
      </tr>
      <tr>
        <td id="L169" class="blob-line-num js-line-number" data-line-number="169"></td>
        <td id="LC169" class="blob-line-code js-file-line">    <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L170" class="blob-line-num js-line-number" data-line-number="170"></td>
        <td id="LC170" class="blob-line-code js-file-line">    <span class="nx">data</span> <span class="o">=</span> <span class="nx">data</span> <span class="o">||</span> <span class="nx">getExpandoData</span><span class="p">(</span><span class="nx">ownerDocument</span><span class="p">);</span></td>
      </tr>
      <tr>
        <td id="L171" class="blob-line-num js-line-number" data-line-number="171"></td>
        <td id="LC171" class="blob-line-code js-file-line">    <span class="kd">var</span> <span class="nx">clone</span> <span class="o">=</span> <span class="nx">data</span><span class="p">.</span><span class="nx">frag</span><span class="p">.</span><span class="nx">cloneNode</span><span class="p">(),</span></td>
      </tr>
      <tr>
        <td id="L172" class="blob-line-num js-line-number" data-line-number="172"></td>
        <td id="LC172" class="blob-line-code js-file-line">        <span class="nx">i</span> <span class="o">=</span> <span class="mi">0</span><span class="p">,</span></td>
      </tr>
      <tr>
        <td id="L173" class="blob-line-num js-line-number" data-line-number="173"></td>
        <td id="LC173" class="blob-line-code js-file-line">        <span class="nx">elems</span> <span class="o">=</span> <span class="nx">getElements</span><span class="p">(),</span></td>
      </tr>
      <tr>
        <td id="L174" class="blob-line-num js-line-number" data-line-number="174"></td>
        <td id="LC174" class="blob-line-code js-file-line">        <span class="nx">l</span> <span class="o">=</span> <span class="nx">elems</span><span class="p">.</span><span class="nx">length</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L175" class="blob-line-num js-line-number" data-line-number="175"></td>
        <td id="LC175" class="blob-line-code js-file-line">    <span class="k">for</span><span class="p">(;</span><span class="nx">i</span><span class="o">&lt;</span><span class="nx">l</span><span class="p">;</span><span class="nx">i</span><span class="o">++</span><span class="p">){</span></td>
      </tr>
      <tr>
        <td id="L176" class="blob-line-num js-line-number" data-line-number="176"></td>
        <td id="LC176" class="blob-line-code js-file-line">        <span class="nx">clone</span><span class="p">.</span><span class="nx">createElement</span><span class="p">(</span><span class="nx">elems</span><span class="p">[</span><span class="nx">i</span><span class="p">]);</span></td>
      </tr>
      <tr>
        <td id="L177" class="blob-line-num js-line-number" data-line-number="177"></td>
        <td id="LC177" class="blob-line-code js-file-line">    <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L178" class="blob-line-num js-line-number" data-line-number="178"></td>
        <td id="LC178" class="blob-line-code js-file-line">    <span class="k">return</span> <span class="nx">clone</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L179" class="blob-line-num js-line-number" data-line-number="179"></td>
        <td id="LC179" class="blob-line-code js-file-line">  <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L180" class="blob-line-num js-line-number" data-line-number="180"></td>
        <td id="LC180" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L181" class="blob-line-num js-line-number" data-line-number="181"></td>
        <td id="LC181" class="blob-line-code js-file-line">  <span class="cm">/**</span></td>
      </tr>
      <tr>
        <td id="L182" class="blob-line-num js-line-number" data-line-number="182"></td>
        <td id="LC182" class="blob-line-code js-file-line"><span class="cm">   * Shivs the `createElement` and `createDocumentFragment` methods of the document.</span></td>
      </tr>
      <tr>
        <td id="L183" class="blob-line-num js-line-number" data-line-number="183"></td>
        <td id="LC183" class="blob-line-code js-file-line"><span class="cm">   * @private</span></td>
      </tr>
      <tr>
        <td id="L184" class="blob-line-num js-line-number" data-line-number="184"></td>
        <td id="LC184" class="blob-line-code js-file-line"><span class="cm">   * @param {Document|DocumentFragment} ownerDocument The document.</span></td>
      </tr>
      <tr>
        <td id="L185" class="blob-line-num js-line-number" data-line-number="185"></td>
        <td id="LC185" class="blob-line-code js-file-line"><span class="cm">   * @param {Object} data of the document.</span></td>
      </tr>
      <tr>
        <td id="L186" class="blob-line-num js-line-number" data-line-number="186"></td>
        <td id="LC186" class="blob-line-code js-file-line"><span class="cm">   */</span></td>
      </tr>
      <tr>
        <td id="L187" class="blob-line-num js-line-number" data-line-number="187"></td>
        <td id="LC187" class="blob-line-code js-file-line">  <span class="kd">function</span> <span class="nx">shivMethods</span><span class="p">(</span><span class="nx">ownerDocument</span><span class="p">,</span> <span class="nx">data</span><span class="p">)</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L188" class="blob-line-num js-line-number" data-line-number="188"></td>
        <td id="LC188" class="blob-line-code js-file-line">    <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="nx">data</span><span class="p">.</span><span class="nx">cache</span><span class="p">)</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L189" class="blob-line-num js-line-number" data-line-number="189"></td>
        <td id="LC189" class="blob-line-code js-file-line">        <span class="nx">data</span><span class="p">.</span><span class="nx">cache</span> <span class="o">=</span> <span class="p">{};</span></td>
      </tr>
      <tr>
        <td id="L190" class="blob-line-num js-line-number" data-line-number="190"></td>
        <td id="LC190" class="blob-line-code js-file-line">        <span class="nx">data</span><span class="p">.</span><span class="nx">createElem</span> <span class="o">=</span> <span class="nx">ownerDocument</span><span class="p">.</span><span class="nx">createElement</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L191" class="blob-line-num js-line-number" data-line-number="191"></td>
        <td id="LC191" class="blob-line-code js-file-line">        <span class="nx">data</span><span class="p">.</span><span class="nx">createFrag</span> <span class="o">=</span> <span class="nx">ownerDocument</span><span class="p">.</span><span class="nx">createDocumentFragment</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L192" class="blob-line-num js-line-number" data-line-number="192"></td>
        <td id="LC192" class="blob-line-code js-file-line">        <span class="nx">data</span><span class="p">.</span><span class="nx">frag</span> <span class="o">=</span> <span class="nx">data</span><span class="p">.</span><span class="nx">createFrag</span><span class="p">();</span></td>
      </tr>
      <tr>
        <td id="L193" class="blob-line-num js-line-number" data-line-number="193"></td>
        <td id="LC193" class="blob-line-code js-file-line">    <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L194" class="blob-line-num js-line-number" data-line-number="194"></td>
        <td id="LC194" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L195" class="blob-line-num js-line-number" data-line-number="195"></td>
        <td id="LC195" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L196" class="blob-line-num js-line-number" data-line-number="196"></td>
        <td id="LC196" class="blob-line-code js-file-line">    <span class="nx">ownerDocument</span><span class="p">.</span><span class="nx">createElement</span> <span class="o">=</span> <span class="kd">function</span><span class="p">(</span><span class="nx">nodeName</span><span class="p">)</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L197" class="blob-line-num js-line-number" data-line-number="197"></td>
        <td id="LC197" class="blob-line-code js-file-line">      <span class="c1">//abort shiv</span></td>
      </tr>
      <tr>
        <td id="L198" class="blob-line-num js-line-number" data-line-number="198"></td>
        <td id="LC198" class="blob-line-code js-file-line">      <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="nx">html5</span><span class="p">.</span><span class="nx">shivMethods</span><span class="p">)</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L199" class="blob-line-num js-line-number" data-line-number="199"></td>
        <td id="LC199" class="blob-line-code js-file-line">          <span class="k">return</span> <span class="nx">data</span><span class="p">.</span><span class="nx">createElem</span><span class="p">(</span><span class="nx">nodeName</span><span class="p">);</span></td>
      </tr>
      <tr>
        <td id="L200" class="blob-line-num js-line-number" data-line-number="200"></td>
        <td id="LC200" class="blob-line-code js-file-line">      <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L201" class="blob-line-num js-line-number" data-line-number="201"></td>
        <td id="LC201" class="blob-line-code js-file-line">      <span class="k">return</span> <span class="nx">createElement</span><span class="p">(</span><span class="nx">nodeName</span><span class="p">,</span> <span class="nx">ownerDocument</span><span class="p">,</span> <span class="nx">data</span><span class="p">);</span></td>
      </tr>
      <tr>
        <td id="L202" class="blob-line-num js-line-number" data-line-number="202"></td>
        <td id="LC202" class="blob-line-code js-file-line">    <span class="p">};</span></td>
      </tr>
      <tr>
        <td id="L203" class="blob-line-num js-line-number" data-line-number="203"></td>
        <td id="LC203" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L204" class="blob-line-num js-line-number" data-line-number="204"></td>
        <td id="LC204" class="blob-line-code js-file-line">    <span class="nx">ownerDocument</span><span class="p">.</span><span class="nx">createDocumentFragment</span> <span class="o">=</span> <span class="nb">Function</span><span class="p">(</span><span class="s1">&#39;h,f&#39;</span><span class="p">,</span> <span class="s1">&#39;return function(){&#39;</span> <span class="o">+</span></td>
      </tr>
      <tr>
        <td id="L205" class="blob-line-num js-line-number" data-line-number="205"></td>
        <td id="LC205" class="blob-line-code js-file-line">      <span class="s1">&#39;var n=f.cloneNode(),c=n.createElement;&#39;</span> <span class="o">+</span></td>
      </tr>
      <tr>
        <td id="L206" class="blob-line-num js-line-number" data-line-number="206"></td>
        <td id="LC206" class="blob-line-code js-file-line">      <span class="s1">&#39;h.shivMethods&amp;&amp;(&#39;</span> <span class="o">+</span></td>
      </tr>
      <tr>
        <td id="L207" class="blob-line-num js-line-number" data-line-number="207"></td>
        <td id="LC207" class="blob-line-code js-file-line">        <span class="c1">// unroll the `createElement` calls</span></td>
      </tr>
      <tr>
        <td id="L208" class="blob-line-num js-line-number" data-line-number="208"></td>
        <td id="LC208" class="blob-line-code js-file-line">        <span class="nx">getElements</span><span class="p">().</span><span class="nx">join</span><span class="p">().</span><span class="nx">replace</span><span class="p">(</span><span class="sr">/[\w\-:]+/g</span><span class="p">,</span> <span class="kd">function</span><span class="p">(</span><span class="nx">nodeName</span><span class="p">)</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L209" class="blob-line-num js-line-number" data-line-number="209"></td>
        <td id="LC209" class="blob-line-code js-file-line">          <span class="nx">data</span><span class="p">.</span><span class="nx">createElem</span><span class="p">(</span><span class="nx">nodeName</span><span class="p">);</span></td>
      </tr>
      <tr>
        <td id="L210" class="blob-line-num js-line-number" data-line-number="210"></td>
        <td id="LC210" class="blob-line-code js-file-line">          <span class="nx">data</span><span class="p">.</span><span class="nx">frag</span><span class="p">.</span><span class="nx">createElement</span><span class="p">(</span><span class="nx">nodeName</span><span class="p">);</span></td>
      </tr>
      <tr>
        <td id="L211" class="blob-line-num js-line-number" data-line-number="211"></td>
        <td id="LC211" class="blob-line-code js-file-line">          <span class="k">return</span> <span class="s1">&#39;c(&quot;&#39;</span> <span class="o">+</span> <span class="nx">nodeName</span> <span class="o">+</span> <span class="s1">&#39;&quot;)&#39;</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L212" class="blob-line-num js-line-number" data-line-number="212"></td>
        <td id="LC212" class="blob-line-code js-file-line">        <span class="p">})</span> <span class="o">+</span></td>
      </tr>
      <tr>
        <td id="L213" class="blob-line-num js-line-number" data-line-number="213"></td>
        <td id="LC213" class="blob-line-code js-file-line">      <span class="s1">&#39;);return n}&#39;</span></td>
      </tr>
      <tr>
        <td id="L214" class="blob-line-num js-line-number" data-line-number="214"></td>
        <td id="LC214" class="blob-line-code js-file-line">    <span class="p">)(</span><span class="nx">html5</span><span class="p">,</span> <span class="nx">data</span><span class="p">.</span><span class="nx">frag</span><span class="p">);</span></td>
      </tr>
      <tr>
        <td id="L215" class="blob-line-num js-line-number" data-line-number="215"></td>
        <td id="LC215" class="blob-line-code js-file-line">  <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L216" class="blob-line-num js-line-number" data-line-number="216"></td>
        <td id="LC216" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L217" class="blob-line-num js-line-number" data-line-number="217"></td>
        <td id="LC217" class="blob-line-code js-file-line">  <span class="cm">/*--------------------------------------------------------------------------*/</span></td>
      </tr>
      <tr>
        <td id="L218" class="blob-line-num js-line-number" data-line-number="218"></td>
        <td id="LC218" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L219" class="blob-line-num js-line-number" data-line-number="219"></td>
        <td id="LC219" class="blob-line-code js-file-line">  <span class="cm">/**</span></td>
      </tr>
      <tr>
        <td id="L220" class="blob-line-num js-line-number" data-line-number="220"></td>
        <td id="LC220" class="blob-line-code js-file-line"><span class="cm">   * Shivs the given document.</span></td>
      </tr>
      <tr>
        <td id="L221" class="blob-line-num js-line-number" data-line-number="221"></td>
        <td id="LC221" class="blob-line-code js-file-line"><span class="cm">   * @memberOf html5</span></td>
      </tr>
      <tr>
        <td id="L222" class="blob-line-num js-line-number" data-line-number="222"></td>
        <td id="LC222" class="blob-line-code js-file-line"><span class="cm">   * @param {Document} ownerDocument The document to shiv.</span></td>
      </tr>
      <tr>
        <td id="L223" class="blob-line-num js-line-number" data-line-number="223"></td>
        <td id="LC223" class="blob-line-code js-file-line"><span class="cm">   * @returns {Document} The shived document.</span></td>
      </tr>
      <tr>
        <td id="L224" class="blob-line-num js-line-number" data-line-number="224"></td>
        <td id="LC224" class="blob-line-code js-file-line"><span class="cm">   */</span></td>
      </tr>
      <tr>
        <td id="L225" class="blob-line-num js-line-number" data-line-number="225"></td>
        <td id="LC225" class="blob-line-code js-file-line">  <span class="kd">function</span> <span class="nx">shivDocument</span><span class="p">(</span><span class="nx">ownerDocument</span><span class="p">)</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L226" class="blob-line-num js-line-number" data-line-number="226"></td>
        <td id="LC226" class="blob-line-code js-file-line">    <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="nx">ownerDocument</span><span class="p">)</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L227" class="blob-line-num js-line-number" data-line-number="227"></td>
        <td id="LC227" class="blob-line-code js-file-line">        <span class="nx">ownerDocument</span> <span class="o">=</span> <span class="nb">document</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L228" class="blob-line-num js-line-number" data-line-number="228"></td>
        <td id="LC228" class="blob-line-code js-file-line">    <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L229" class="blob-line-num js-line-number" data-line-number="229"></td>
        <td id="LC229" class="blob-line-code js-file-line">    <span class="kd">var</span> <span class="nx">data</span> <span class="o">=</span> <span class="nx">getExpandoData</span><span class="p">(</span><span class="nx">ownerDocument</span><span class="p">);</span></td>
      </tr>
      <tr>
        <td id="L230" class="blob-line-num js-line-number" data-line-number="230"></td>
        <td id="LC230" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L231" class="blob-line-num js-line-number" data-line-number="231"></td>
        <td id="LC231" class="blob-line-code js-file-line">    <span class="k">if</span> <span class="p">(</span><span class="nx">html5</span><span class="p">.</span><span class="nx">shivCSS</span> <span class="o">&amp;&amp;</span> <span class="o">!</span><span class="nx">supportsHtml5Styles</span> <span class="o">&amp;&amp;</span> <span class="o">!</span><span class="nx">data</span><span class="p">.</span><span class="nx">hasCSS</span><span class="p">)</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L232" class="blob-line-num js-line-number" data-line-number="232"></td>
        <td id="LC232" class="blob-line-code js-file-line">      <span class="nx">data</span><span class="p">.</span><span class="nx">hasCSS</span> <span class="o">=</span> <span class="o">!!</span><span class="nx">addStyleSheet</span><span class="p">(</span><span class="nx">ownerDocument</span><span class="p">,</span></td>
      </tr>
      <tr>
        <td id="L233" class="blob-line-num js-line-number" data-line-number="233"></td>
        <td id="LC233" class="blob-line-code js-file-line">        <span class="c1">// corrects block display not defined in IE6/7/8/9</span></td>
      </tr>
      <tr>
        <td id="L234" class="blob-line-num js-line-number" data-line-number="234"></td>
        <td id="LC234" class="blob-line-code js-file-line">        <span class="s1">&#39;article,aside,dialog,figcaption,figure,footer,header,hgroup,main,nav,section{display:block}&#39;</span> <span class="o">+</span></td>
      </tr>
      <tr>
        <td id="L235" class="blob-line-num js-line-number" data-line-number="235"></td>
        <td id="LC235" class="blob-line-code js-file-line">        <span class="c1">// adds styling not present in IE6/7/8/9</span></td>
      </tr>
      <tr>
        <td id="L236" class="blob-line-num js-line-number" data-line-number="236"></td>
        <td id="LC236" class="blob-line-code js-file-line">        <span class="s1">&#39;mark{background:#FF0;color:#000}&#39;</span> <span class="o">+</span></td>
      </tr>
      <tr>
        <td id="L237" class="blob-line-num js-line-number" data-line-number="237"></td>
        <td id="LC237" class="blob-line-code js-file-line">        <span class="c1">// hides non-rendered elements</span></td>
      </tr>
      <tr>
        <td id="L238" class="blob-line-num js-line-number" data-line-number="238"></td>
        <td id="LC238" class="blob-line-code js-file-line">        <span class="s1">&#39;template{display:none}&#39;</span></td>
      </tr>
      <tr>
        <td id="L239" class="blob-line-num js-line-number" data-line-number="239"></td>
        <td id="LC239" class="blob-line-code js-file-line">      <span class="p">);</span></td>
      </tr>
      <tr>
        <td id="L240" class="blob-line-num js-line-number" data-line-number="240"></td>
        <td id="LC240" class="blob-line-code js-file-line">    <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L241" class="blob-line-num js-line-number" data-line-number="241"></td>
        <td id="LC241" class="blob-line-code js-file-line">    <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="nx">supportsUnknownElements</span><span class="p">)</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L242" class="blob-line-num js-line-number" data-line-number="242"></td>
        <td id="LC242" class="blob-line-code js-file-line">      <span class="nx">shivMethods</span><span class="p">(</span><span class="nx">ownerDocument</span><span class="p">,</span> <span class="nx">data</span><span class="p">);</span></td>
      </tr>
      <tr>
        <td id="L243" class="blob-line-num js-line-number" data-line-number="243"></td>
        <td id="LC243" class="blob-line-code js-file-line">    <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L244" class="blob-line-num js-line-number" data-line-number="244"></td>
        <td id="LC244" class="blob-line-code js-file-line">    <span class="k">return</span> <span class="nx">ownerDocument</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L245" class="blob-line-num js-line-number" data-line-number="245"></td>
        <td id="LC245" class="blob-line-code js-file-line">  <span class="p">}</span></td>
      </tr>
      <tr>
        <td id="L246" class="blob-line-num js-line-number" data-line-number="246"></td>
        <td id="LC246" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L247" class="blob-line-num js-line-number" data-line-number="247"></td>
        <td id="LC247" class="blob-line-code js-file-line">  <span class="cm">/*--------------------------------------------------------------------------*/</span></td>
      </tr>
      <tr>
        <td id="L248" class="blob-line-num js-line-number" data-line-number="248"></td>
        <td id="LC248" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L249" class="blob-line-num js-line-number" data-line-number="249"></td>
        <td id="LC249" class="blob-line-code js-file-line">  <span class="cm">/**</span></td>
      </tr>
      <tr>
        <td id="L250" class="blob-line-num js-line-number" data-line-number="250"></td>
        <td id="LC250" class="blob-line-code js-file-line"><span class="cm">   * The `html5` object is exposed so that more elements can be shived and</span></td>
      </tr>
      <tr>
        <td id="L251" class="blob-line-num js-line-number" data-line-number="251"></td>
        <td id="LC251" class="blob-line-code js-file-line"><span class="cm">   * existing shiving can be detected on iframes.</span></td>
      </tr>
      <tr>
        <td id="L252" class="blob-line-num js-line-number" data-line-number="252"></td>
        <td id="LC252" class="blob-line-code js-file-line"><span class="cm">   * @type Object</span></td>
      </tr>
      <tr>
        <td id="L253" class="blob-line-num js-line-number" data-line-number="253"></td>
        <td id="LC253" class="blob-line-code js-file-line"><span class="cm">   * @example</span></td>
      </tr>
      <tr>
        <td id="L254" class="blob-line-num js-line-number" data-line-number="254"></td>
        <td id="LC254" class="blob-line-code js-file-line"><span class="cm">   *</span></td>
      </tr>
      <tr>
        <td id="L255" class="blob-line-num js-line-number" data-line-number="255"></td>
        <td id="LC255" class="blob-line-code js-file-line"><span class="cm">   * // options can be changed before the script is included</span></td>
      </tr>
      <tr>
        <td id="L256" class="blob-line-num js-line-number" data-line-number="256"></td>
        <td id="LC256" class="blob-line-code js-file-line"><span class="cm">   * html5 = { &#39;elements&#39;: &#39;mark section&#39;, &#39;shivCSS&#39;: false, &#39;shivMethods&#39;: false };</span></td>
      </tr>
      <tr>
        <td id="L257" class="blob-line-num js-line-number" data-line-number="257"></td>
        <td id="LC257" class="blob-line-code js-file-line"><span class="cm">   */</span></td>
      </tr>
      <tr>
        <td id="L258" class="blob-line-num js-line-number" data-line-number="258"></td>
        <td id="LC258" class="blob-line-code js-file-line">  <span class="kd">var</span> <span class="nx">html5</span> <span class="o">=</span> <span class="p">{</span></td>
      </tr>
      <tr>
        <td id="L259" class="blob-line-num js-line-number" data-line-number="259"></td>
        <td id="LC259" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L260" class="blob-line-num js-line-number" data-line-number="260"></td>
        <td id="LC260" class="blob-line-code js-file-line">    <span class="cm">/**</span></td>
      </tr>
      <tr>
        <td id="L261" class="blob-line-num js-line-number" data-line-number="261"></td>
        <td id="LC261" class="blob-line-code js-file-line"><span class="cm">     * An array or space separated string of node names of the elements to shiv.</span></td>
      </tr>
      <tr>
        <td id="L262" class="blob-line-num js-line-number" data-line-number="262"></td>
        <td id="LC262" class="blob-line-code js-file-line"><span class="cm">     * @memberOf html5</span></td>
      </tr>
      <tr>
        <td id="L263" class="blob-line-num js-line-number" data-line-number="263"></td>
        <td id="LC263" class="blob-line-code js-file-line"><span class="cm">     * @type Array|String</span></td>
      </tr>
      <tr>
        <td id="L264" class="blob-line-num js-line-number" data-line-number="264"></td>
        <td id="LC264" class="blob-line-code js-file-line"><span class="cm">     */</span></td>
      </tr>
      <tr>
        <td id="L265" class="blob-line-num js-line-number" data-line-number="265"></td>
        <td id="LC265" class="blob-line-code js-file-line">    <span class="s1">&#39;elements&#39;</span><span class="o">:</span> <span class="nx">options</span><span class="p">.</span><span class="nx">elements</span> <span class="o">||</span> <span class="s1">&#39;abbr article aside audio bdi canvas data datalist details dialog figcaption figure footer header hgroup main mark meter nav output picture progress section summary template time video&#39;</span><span class="p">,</span></td>
      </tr>
      <tr>
        <td id="L266" class="blob-line-num js-line-number" data-line-number="266"></td>
        <td id="LC266" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L267" class="blob-line-num js-line-number" data-line-number="267"></td>
        <td id="LC267" class="blob-line-code js-file-line">    <span class="cm">/**</span></td>
      </tr>
      <tr>
        <td id="L268" class="blob-line-num js-line-number" data-line-number="268"></td>
        <td id="LC268" class="blob-line-code js-file-line"><span class="cm">     * current version of html5shiv</span></td>
      </tr>
      <tr>
        <td id="L269" class="blob-line-num js-line-number" data-line-number="269"></td>
        <td id="LC269" class="blob-line-code js-file-line"><span class="cm">     */</span></td>
      </tr>
      <tr>
        <td id="L270" class="blob-line-num js-line-number" data-line-number="270"></td>
        <td id="LC270" class="blob-line-code js-file-line">    <span class="s1">&#39;version&#39;</span><span class="o">:</span> <span class="nx">version</span><span class="p">,</span></td>
      </tr>
      <tr>
        <td id="L271" class="blob-line-num js-line-number" data-line-number="271"></td>
        <td id="LC271" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L272" class="blob-line-num js-line-number" data-line-number="272"></td>
        <td id="LC272" class="blob-line-code js-file-line">    <span class="cm">/**</span></td>
      </tr>
      <tr>
        <td id="L273" class="blob-line-num js-line-number" data-line-number="273"></td>
        <td id="LC273" class="blob-line-code js-file-line"><span class="cm">     * A flag to indicate that the HTML5 style sheet should be inserted.</span></td>
      </tr>
      <tr>
        <td id="L274" class="blob-line-num js-line-number" data-line-number="274"></td>
        <td id="LC274" class="blob-line-code js-file-line"><span class="cm">     * @memberOf html5</span></td>
      </tr>
      <tr>
        <td id="L275" class="blob-line-num js-line-number" data-line-number="275"></td>
        <td id="LC275" class="blob-line-code js-file-line"><span class="cm">     * @type Boolean</span></td>
      </tr>
      <tr>
        <td id="L276" class="blob-line-num js-line-number" data-line-number="276"></td>
        <td id="LC276" class="blob-line-code js-file-line"><span class="cm">     */</span></td>
      </tr>
      <tr>
        <td id="L277" class="blob-line-num js-line-number" data-line-number="277"></td>
        <td id="LC277" class="blob-line-code js-file-line">    <span class="s1">&#39;shivCSS&#39;</span><span class="o">:</span> <span class="p">(</span><span class="nx">options</span><span class="p">.</span><span class="nx">shivCSS</span> <span class="o">!==</span> <span class="kc">false</span><span class="p">),</span></td>
      </tr>
      <tr>
        <td id="L278" class="blob-line-num js-line-number" data-line-number="278"></td>
        <td id="LC278" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L279" class="blob-line-num js-line-number" data-line-number="279"></td>
        <td id="LC279" class="blob-line-code js-file-line">    <span class="cm">/**</span></td>
      </tr>
      <tr>
        <td id="L280" class="blob-line-num js-line-number" data-line-number="280"></td>
        <td id="LC280" class="blob-line-code js-file-line"><span class="cm">     * Is equal to true if a browser supports creating unknown/HTML5 elements</span></td>
      </tr>
      <tr>
        <td id="L281" class="blob-line-num js-line-number" data-line-number="281"></td>
        <td id="LC281" class="blob-line-code js-file-line"><span class="cm">     * @memberOf html5</span></td>
      </tr>
      <tr>
        <td id="L282" class="blob-line-num js-line-number" data-line-number="282"></td>
        <td id="LC282" class="blob-line-code js-file-line"><span class="cm">     * @type boolean</span></td>
      </tr>
      <tr>
        <td id="L283" class="blob-line-num js-line-number" data-line-number="283"></td>
        <td id="LC283" class="blob-line-code js-file-line"><span class="cm">     */</span></td>
      </tr>
      <tr>
        <td id="L284" class="blob-line-num js-line-number" data-line-number="284"></td>
        <td id="LC284" class="blob-line-code js-file-line">    <span class="s1">&#39;supportsUnknownElements&#39;</span><span class="o">:</span> <span class="nx">supportsUnknownElements</span><span class="p">,</span></td>
      </tr>
      <tr>
        <td id="L285" class="blob-line-num js-line-number" data-line-number="285"></td>
        <td id="LC285" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L286" class="blob-line-num js-line-number" data-line-number="286"></td>
        <td id="LC286" class="blob-line-code js-file-line">    <span class="cm">/**</span></td>
      </tr>
      <tr>
        <td id="L287" class="blob-line-num js-line-number" data-line-number="287"></td>
        <td id="LC287" class="blob-line-code js-file-line"><span class="cm">     * A flag to indicate that the document&#39;s `createElement` and `createDocumentFragment`</span></td>
      </tr>
      <tr>
        <td id="L288" class="blob-line-num js-line-number" data-line-number="288"></td>
        <td id="LC288" class="blob-line-code js-file-line"><span class="cm">     * methods should be overwritten.</span></td>
      </tr>
      <tr>
        <td id="L289" class="blob-line-num js-line-number" data-line-number="289"></td>
        <td id="LC289" class="blob-line-code js-file-line"><span class="cm">     * @memberOf html5</span></td>
      </tr>
      <tr>
        <td id="L290" class="blob-line-num js-line-number" data-line-number="290"></td>
        <td id="LC290" class="blob-line-code js-file-line"><span class="cm">     * @type Boolean</span></td>
      </tr>
      <tr>
        <td id="L291" class="blob-line-num js-line-number" data-line-number="291"></td>
        <td id="LC291" class="blob-line-code js-file-line"><span class="cm">     */</span></td>
      </tr>
      <tr>
        <td id="L292" class="blob-line-num js-line-number" data-line-number="292"></td>
        <td id="LC292" class="blob-line-code js-file-line">    <span class="s1">&#39;shivMethods&#39;</span><span class="o">:</span> <span class="p">(</span><span class="nx">options</span><span class="p">.</span><span class="nx">shivMethods</span> <span class="o">!==</span> <span class="kc">false</span><span class="p">),</span></td>
      </tr>
      <tr>
        <td id="L293" class="blob-line-num js-line-number" data-line-number="293"></td>
        <td id="LC293" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L294" class="blob-line-num js-line-number" data-line-number="294"></td>
        <td id="LC294" class="blob-line-code js-file-line">    <span class="cm">/**</span></td>
      </tr>
      <tr>
        <td id="L295" class="blob-line-num js-line-number" data-line-number="295"></td>
        <td id="LC295" class="blob-line-code js-file-line"><span class="cm">     * A string to describe the type of `html5` object (&quot;default&quot; or &quot;default print&quot;).</span></td>
      </tr>
      <tr>
        <td id="L296" class="blob-line-num js-line-number" data-line-number="296"></td>
        <td id="LC296" class="blob-line-code js-file-line"><span class="cm">     * @memberOf html5</span></td>
      </tr>
      <tr>
        <td id="L297" class="blob-line-num js-line-number" data-line-number="297"></td>
        <td id="LC297" class="blob-line-code js-file-line"><span class="cm">     * @type String</span></td>
      </tr>
      <tr>
        <td id="L298" class="blob-line-num js-line-number" data-line-number="298"></td>
        <td id="LC298" class="blob-line-code js-file-line"><span class="cm">     */</span></td>
      </tr>
      <tr>
        <td id="L299" class="blob-line-num js-line-number" data-line-number="299"></td>
        <td id="LC299" class="blob-line-code js-file-line">    <span class="s1">&#39;type&#39;</span><span class="o">:</span> <span class="s1">&#39;default&#39;</span><span class="p">,</span></td>
      </tr>
      <tr>
        <td id="L300" class="blob-line-num js-line-number" data-line-number="300"></td>
        <td id="LC300" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L301" class="blob-line-num js-line-number" data-line-number="301"></td>
        <td id="LC301" class="blob-line-code js-file-line">    <span class="c1">// shivs the document according to the specified `html5` object options</span></td>
      </tr>
      <tr>
        <td id="L302" class="blob-line-num js-line-number" data-line-number="302"></td>
        <td id="LC302" class="blob-line-code js-file-line">    <span class="s1">&#39;shivDocument&#39;</span><span class="o">:</span> <span class="nx">shivDocument</span><span class="p">,</span></td>
      </tr>
      <tr>
        <td id="L303" class="blob-line-num js-line-number" data-line-number="303"></td>
        <td id="LC303" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L304" class="blob-line-num js-line-number" data-line-number="304"></td>
        <td id="LC304" class="blob-line-code js-file-line">    <span class="c1">//creates a shived element</span></td>
      </tr>
      <tr>
        <td id="L305" class="blob-line-num js-line-number" data-line-number="305"></td>
        <td id="LC305" class="blob-line-code js-file-line">    <span class="nx">createElement</span><span class="o">:</span> <span class="nx">createElement</span><span class="p">,</span></td>
      </tr>
      <tr>
        <td id="L306" class="blob-line-num js-line-number" data-line-number="306"></td>
        <td id="LC306" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L307" class="blob-line-num js-line-number" data-line-number="307"></td>
        <td id="LC307" class="blob-line-code js-file-line">    <span class="c1">//creates a shived documentFragment</span></td>
      </tr>
      <tr>
        <td id="L308" class="blob-line-num js-line-number" data-line-number="308"></td>
        <td id="LC308" class="blob-line-code js-file-line">    <span class="nx">createDocumentFragment</span><span class="o">:</span> <span class="nx">createDocumentFragment</span><span class="p">,</span></td>
      </tr>
      <tr>
        <td id="L309" class="blob-line-num js-line-number" data-line-number="309"></td>
        <td id="LC309" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L310" class="blob-line-num js-line-number" data-line-number="310"></td>
        <td id="LC310" class="blob-line-code js-file-line">    <span class="c1">//extends list of elements</span></td>
      </tr>
      <tr>
        <td id="L311" class="blob-line-num js-line-number" data-line-number="311"></td>
        <td id="LC311" class="blob-line-code js-file-line">    <span class="nx">addElements</span><span class="o">:</span> <span class="nx">addElements</span></td>
      </tr>
      <tr>
        <td id="L312" class="blob-line-num js-line-number" data-line-number="312"></td>
        <td id="LC312" class="blob-line-code js-file-line">  <span class="p">};</span></td>
      </tr>
      <tr>
        <td id="L313" class="blob-line-num js-line-number" data-line-number="313"></td>
        <td id="LC313" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L314" class="blob-line-num js-line-number" data-line-number="314"></td>
        <td id="LC314" class="blob-line-code js-file-line">  <span class="cm">/*--------------------------------------------------------------------------*/</span></td>
      </tr>
      <tr>
        <td id="L315" class="blob-line-num js-line-number" data-line-number="315"></td>
        <td id="LC315" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L316" class="blob-line-num js-line-number" data-line-number="316"></td>
        <td id="LC316" class="blob-line-code js-file-line">  <span class="c1">// expose html5</span></td>
      </tr>
      <tr>
        <td id="L317" class="blob-line-num js-line-number" data-line-number="317"></td>
        <td id="LC317" class="blob-line-code js-file-line">  <span class="nb">window</span><span class="p">.</span><span class="nx">html5</span> <span class="o">=</span> <span class="nx">html5</span><span class="p">;</span></td>
      </tr>
      <tr>
        <td id="L318" class="blob-line-num js-line-number" data-line-number="318"></td>
        <td id="LC318" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L319" class="blob-line-num js-line-number" data-line-number="319"></td>
        <td id="LC319" class="blob-line-code js-file-line">  <span class="c1">// shiv the document</span></td>
      </tr>
      <tr>
        <td id="L320" class="blob-line-num js-line-number" data-line-number="320"></td>
        <td id="LC320" class="blob-line-code js-file-line">  <span class="nx">shivDocument</span><span class="p">(</span><span class="nb">document</span><span class="p">);</span></td>
      </tr>
      <tr>
        <td id="L321" class="blob-line-num js-line-number" data-line-number="321"></td>
        <td id="LC321" class="blob-line-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L322" class="blob-line-num js-line-number" data-line-number="322"></td>
        <td id="LC322" class="blob-line-code js-file-line"><span class="p">}(</span><span class="k">this</span><span class="p">,</span> <span class="nb">document</span><span class="p">));</span></td>
      </tr>
</table>

  </div>

  </div>
</div>

<a href="#jump-to-line" rel="facebox[.linejump]" data-hotkey="l" style="display:none">Jump to Line</a>
<div id="jump-to-line" style="display:none">
  <form accept-charset="UTF-8" class="js-jump-to-line-form">
    <input class="linejump-input js-jump-to-line-field" type="text" placeholder="Jump to line&hellip;" autofocus>
    <button type="submit" class="button">Go</button>
  </form>
</div>

        </div>

      </div><!-- /.repo-container -->
      <div class="modal-backdrop"></div>
    </div><!-- /.container -->
  </div><!-- /.site -->


    </div><!-- /.wrapper -->

      <div class="container">
  <div class="site-footer">
    <ul class="site-footer-links right">
      <li><a href="https://status.github.com/">Status</a></li>
      <li><a href="http://developer.github.com">API</a></li>
      <li><a href="http://training.github.com">Training</a></li>
      <li><a href="http://shop.github.com">Shop</a></li>
      <li><a href="/blog">Blog</a></li>
      <li><a href="/about">About</a></li>

    </ul>

    <a href="/" aria-label="Homepage">
      <span class="mega-octicon octicon-mark-github" title="GitHub"></span>
    </a>

    <ul class="site-footer-links">
      <li>&copy; 2014 <span title="0.02747s from github-fe123-cp1-prd.iad.github.net">GitHub</span>, Inc.</li>
        <li><a href="/site/terms">Terms</a></li>
        <li><a href="/site/privacy">Privacy</a></li>
        <li><a href="/security">Security</a></li>
        <li><a href="/contact">Contact</a></li>
    </ul>
  </div><!-- /.site-footer -->
</div><!-- /.container -->


    <div class="fullscreen-overlay js-fullscreen-overlay" id="fullscreen_overlay">
  <div class="fullscreen-container js-suggester-container">
    <div class="textarea-wrap">
      <textarea name="fullscreen-contents" id="fullscreen-contents" class="fullscreen-contents js-fullscreen-contents js-suggester-field" placeholder=""></textarea>
    </div>
  </div>
  <div class="fullscreen-sidebar">
    <a href="#" class="exit-fullscreen js-exit-fullscreen tooltipped tooltipped-w" aria-label="Exit Zen Mode">
      <span class="mega-octicon octicon-screen-normal"></span>
    </a>
    <a href="#" class="theme-switcher js-theme-switcher tooltipped tooltipped-w"
      aria-label="Switch themes">
      <span class="octicon octicon-color-mode"></span>
    </a>
  </div>
</div>



    <div id="ajax-error-message" class="flash flash-error">
      <span class="octicon octicon-alert"></span>
      <a href="#" class="octicon octicon-x close js-ajax-error-dismiss" aria-label="Dismiss error"></a>
      Something went wrong with that request. Please try again.
    </div>


      <script crossorigin="anonymous" src="https://assets-cdn.github.com/assets/frameworks-12d5fda141e78e513749dddbc56445fe172cbd9a.js" type="text/javascript"></script>
      <script async="async" crossorigin="anonymous" src="https://assets-cdn.github.com/assets/github-73863815e69f006dc46f81b2538598f55c3602ff.js" type="text/javascript"></script>
      
      
        <script async src="https://www.google-analytics.com/analytics.js"></script>
  </body>
</html>

