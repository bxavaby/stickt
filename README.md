# Stickt

<p>Interactive AI sticker generator using Replicate's <code>fofr/sticker-maker</code> model.</p>

<h2>Setup & Run</h2>

<pre><code>git clone &lt;https://github.com/bxavaby/stickt&gt; && cd stickt
chmod +x install.sh && ./install.sh
# Edit .env with your Replicate API token
source venv/bin/activate && python icky.py</code></pre>

<h2>Features</h2>

<ul>
<li><strong>8 aspect ratios</strong> - Square, portrait, landscape, wide, other formats</li>
<li><strong>WebP/PNG output</strong> - Choose file format</li>
<li><strong>Interactive prompts</strong> - Clean step-by-step interface</li>
<li><strong>Auto preview</strong> - Opens generated stickers with xdg-open</li>
<li><strong>Batch workflow</strong> - Generate multiple stickers in one session</li>
</ul>

<p>Stickers saved to <code>./stickers/</code> directory.</p>

<p><strong>Requirements:</strong> Python 3.8+, Replicate API token</p>

<hr>

<p><em>Get your API token at <a href="https://replicate.com">replicate.com</a></em></p>
