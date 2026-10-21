WYZ / FIELD NOTES — bilingual static technical blog

FILES
  index.html    Self-contained HTML, CSS, inline SVG and JavaScript.
  .nojekyll     Static publishing marker.
  assets/       Eight research figures, fifteen MP4s and their poster images.

PREVIEW
  Open index.html in a browser or serve this directory with a static web server.
  There are no packages to install and no build step. The complete English
  article is present in the HTML and remains readable without JavaScript.

PUBLISHING PATH
  Wyz000/Wyz000.github.io
  /blog/gpt6-astra-navigation/index.html
  /blog/gpt6-astra-navigation/assets/*

LANGUAGE
  English is the default for a first visit. The EN / 中文 buttons translate the
  full article and interface and remember the selection locally.
  Share ?lang=en or ?lang=zh. Section anchors can be appended, for example:
    /blog/gpt6-astra-navigation/?lang=zh#citywalk
  #en and #zh are also supported.

MEDIA
  Recordings are numbered in original article order: demo-01.mp4 … demo-15.mp4.
  Posters are demo-01-poster.jpg … demo-15-poster.jpg.
  Figures are figure-01.png … figure-08.png.
  Videos are not downloaded before the reader starts playback (preload="none").
  A failed media load falls back to a link to the original Feishu document.
  window.DEMO_ASSETS and window.FIGURE_ASSETS configure paths. A null video
  entry retains the source link without attempting to load an absent file.

CONTENT MAINTENANCE
  English and Chinese text is held in the CONTENT object in index.html.
  The initial HTML is an English snapshot for search engines and readers with
  JavaScript disabled. When updating content, update both the relevant CONTENT
  entry and the corresponding initial HTML section. Keep both languages in sync.
  DEMOS contains titles, original filenames, durations, dimensions and groups.
  Preserve IDs when editing so table-of-contents, references and shared section
  links continue to work.

SOURCE
  https://ucno6p0c7gsx.feishu.cn/wiki/Zo77wK7Dxips1YkT4l0c2fGWnEf?create_from=create_doc_to_wiki
  GitHub identity: https://github.com/Wyz000

The article preserves all three research sections, the introduction, conclusion,
eight figures, fifteen recordings and ten references from the original source.
The header route illustration is explicitly labelled conceptual; it is separate
from the research figures. Figure labels follow the source, including repeated
numbers across sections. The video duration shown is the media playback length,
not the duration of the experiment it illustrates.
