<script lang="ts">
  import { convertUrl, type BlogPost } from '$lib/api';
  import {
    Loader2,
    ArrowRight,
    Wand2,
    FileText,
    Sparkles,
    AlertCircle,
  } from 'lucide-svelte';
  import { marked } from 'marked';

  let url = $state('');
  let loading = $state(false);
  let progressMessage = $state('Processing');
  let blogPost = $state<BlogPost | null>(null);
  let error = $state<string | null>(null);
  let progressTimer: any;

  async function handleSubmit(e: Event) {
    e.preventDefault();
    if (!url) return;

    loading = true;
    progressMessage = 'Processing';
    error = null;
    blogPost = null;

    // Show a patience message if it takes too long (common with free models)
    progressTimer = setTimeout(() => {
      progressMessage = 'Still working... AI can take a moment';
    }, 8000);

    try {
      blogPost = await convertUrl(url);
    } catch (err: any) {
      error = err.message || 'An unexpected error occurred';
    } finally {
      clearTimeout(progressTimer);
      loading = false;
    }
  }

  function copyToClipboard() {
    if (blogPost) {
      navigator.clipboard.writeText(blogPost.content);
      alert('Copied to clipboard!');
    }
  }
</script>

<div
  class="min-h-screen bg-gray-50 text-gray-900 font-sans selection:bg-indigo-100 selection:text-indigo-900"
>
  <div class="max-w-4xl mx-auto px-6 py-12 md:py-20">
    <header class="text-center mb-12 fade-in">
      <div
        class="inline-flex items-center justify-center p-3 mb-6 rounded-2xl bg-white shadow-xl shadow-indigo-100 ring-1 ring-black/5"
      >
        <Wand2 class="w-8 h-8 text-indigo-600" />
      </div>
      <h1
        class="text-4xl md:text-5xl font-extrabold tracking-tight mb-4 bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-violet-600"
      >
        URL to Blog Converter
      </h1>
      <p class="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
        Transform any webpage into a perfectly structured, engaging blog post in
        seconds using AI.
      </p>
    </header>

    <div
      class="bg-white rounded-3xl shadow-2xl shadow-gray-200/50 p-2 ring-1 ring-gray-100 mb-12 transform transition-all hover:scale-[1.01] duration-300"
    >
      <form onsubmit={handleSubmit} class="relative flex items-center">
        <div class="absolute left-6 text-gray-400">
          <Sparkles class="w-5 h-5" />
        </div>
        <input
          type="url"
          bind:value={url}
          placeholder="Paste a URL to convert (e.g. https://example.com/article)"
          class="w-full pl-14 pr-32 py-5 text-lg bg-transparent border-0 focus:outline-none placeholder:text-gray-400 text-gray-900 rounded-2xl"
          required
        />
        <button
          type="submit"
          disabled={loading || !url}
          class="absolute right-2 top-2 bottom-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-200 disabled:cursor-not-allowed text-white font-semibold rounded-xl px-6 transition-all duration-200 flex items-center gap-2 group shadow-lg shadow-indigo-600/20"
        >
          {#if loading}
            <Loader2 class="w-5 h-5 animate-spin" />
            <span>{progressMessage}</span>
          {:else}
            <span>Convert</span>
            <ArrowRight
              class="w-4 h-4 group-hover:translate-x-1 transition-transform"
            />
          {/if}
        </button>
      </form>
    </div>

    {#if error}
      <div
        class="rounded-2xl bg-red-50 p-6 mb-12 flex items-start gap-4 text-red-700 border border-red-100 animate-fade-up"
      >
        <AlertCircle class="w-6 h-6 shrink-0 mt-0.5" />
        <div>
          <h3 class="font-bold text-lg mb-1">Conversion Failed</h3>
          <p class="text-red-600/90">{error}</p>
        </div>
      </div>
    {/if}

    {#if blogPost}
      <article
        class="bg-white rounded-[2rem] shadow-xl shadow-gray-200/50 overflow-hidden animate-fade-up ring-1 ring-gray-100"
      >
        <div
          class="bg-gradient-to-br from-indigo-50 via-white to-violet-50 p-8 md:p-12 border-b border-gray-100"
        >
          {#if blogPost.tags && blogPost.tags.length > 0}
            <div class="flex flex-wrap gap-2 mb-6">
              {#each blogPost.tags as tag}
                <span
                  class="px-3 py-1 rounded-full bg-white text-indigo-600 text-sm font-semibold shadow-sm ring-1 ring-indigo-100 tracking-wide"
                >
                  #{tag}
                </span>
              {/each}
            </div>
          {/if}
          <h2
            class="text-3xl md:text-5xl font-bold text-gray-900 mb-6 leading-tight tracking-tight"
          >
            {blogPost.title}
          </h2>
          <p class="text-xl text-gray-600 leading-relaxed max-w-3xl">
            {blogPost.summary}
          </p>
        </div>

        <div class="p-8 md:p-12 prose prose-lg prose-indigo max-w-none">
          {@html marked.parse(blogPost.content)}
        </div>

        <div class="bg-gray-50 border-t border-gray-100 p-8 flex justify-end">
          <button
            onclick={copyToClipboard}
            class="text-indigo-600 font-semibold hover:text-indigo-800 flex items-center gap-2 transition-colors"
          >
            <FileText class="w-4 h-4" />
            <span>Copy to Clipboard</span>
          </button>
        </div>
      </article>
    {/if}
  </div>
</div>
