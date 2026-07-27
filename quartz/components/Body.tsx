import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const Body: QuartzComponent = ({ children }: QuartzComponentProps) => {
  return (
    <div id="quartz-body">
      {children}
      <div
        dangerouslySetInnerHTML={{
          __html: `
            <div id="quartz-banner">
              <div class="banner-left">
                <button class="banner-btn" onclick="window.location.href='/'" aria-label="返回首页">🏠 首页</button>
                <button class="banner-btn" onclick="window.history.back()" aria-label="返回上一页">⬅ 返回</button>
                <button class="banner-btn" onclick="event.preventDefault();var t=document.getElementById('toast');if(t){t.textContent='请使用 Ctrl+D（Mac: ⌘+D）将本站添加到收藏夹';t.classList.add('show');setTimeout(function(){t.classList.remove('show')},3000);}" aria-label="收藏本站">⭐ 收藏</button>
              </div>
              <div class="banner-center">
                <a href="/" aria-label="返回首页" class="banner-title-link">
                  ROSA★绒花计划Wiki
                </a>
              </div>
              <div class="banner-right">
                <div class="search">
                  <button class="search-button" aria-label="搜索" aria-expanded="false">
                    <svg role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 19.9 19.7">
                      <title>Search</title>
                      <g class="search-path" fill="none">
                        <path stroke-linecap="square" d="M18.5 18.3l-5.4-5.4" />
                        <circle cx="8" cy="8" r="7" />
                      </g>
                    </svg>
                    <p>搜索</p>
                  </button>
                  <div class="search-container">
                    <div class="search-space">
                      <input autocomplete="off" class="search-bar" name="search" type="text" aria-label="搜索内容..." placeholder="搜索内容..." />
                      <div class="search-layout" data-preview="true" data-field-priority='["title","content","tags"]'></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          `,
        }}
      />
      <div
        dangerouslySetInnerHTML={{
          __html: `<button id="back-to-top" onclick="window.scrollTo(0, 0)" aria-label="回到顶部">⬆</button>`,
        }}
      />
      <div
        dangerouslySetInnerHTML={{
          __html: `<button id="share-btn" onclick="event.preventDefault();var url=window.location.href;if(navigator.share){navigator.share({title:document.title,url:url}).catch(function(){});}else{navigator.clipboard.writeText(url).then(function(){var t=document.getElementById('toast');if(t){t.textContent='链接已复制到剪贴板';t.classList.add('show');setTimeout(function(){t.classList.remove('show')},3000);}}).catch(function(){var t=document.getElementById('toast');if(t){t.textContent='复制失败，请手动复制地址栏链接';t.classList.add('show');setTimeout(function(){t.classList.remove('show')},3000);}});}" aria-label="分享本页">📤</button><div id="toast" class="toast-notification"></div>`,
        }}
      />
      <script
        dangerouslySetInnerHTML={{
          __html: `
            (function() {
              if (window.__backToTopInitialized) return;
              window.__backToTopInitialized = true;
              document.addEventListener('DOMContentLoaded', function() {
                var backBtn = document.getElementById('back-to-top');
                var shareBtn = document.getElementById('share-btn');
                window.addEventListener('scroll', function() {
                  if (window.scrollY > 300) {
                    if (backBtn) backBtn.classList.add('visible');
                    if (shareBtn) shareBtn.classList.add('visible');
                  } else {
                    if (backBtn) backBtn.classList.remove('visible');
                    if (shareBtn) shareBtn.classList.remove('visible');
                  }
                });
              });
            })();
          `,
        }}
      />
    </div>
  )
}

export default (() => Body) satisfies QuartzComponentConstructor
