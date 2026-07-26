import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const Body: QuartzComponent = ({ children }: QuartzComponentProps) => {
  return (
    <div id="quartz-body">
      {children}
      <div
        dangerouslySetInnerHTML={{
          __html: `<button id="back-to-top" onclick="window.scrollTo(0, 0)" aria-label="回到顶部">↑</button>`,
        }}
      />
      <script
        dangerouslySetInnerHTML={{
          __html: `
            (function() {
              if (window.__backToTopInitialized) return;
              window.__backToTopInitialized = true;
              document.addEventListener('DOMContentLoaded', function() {
                var btn = document.getElementById('back-to-top');
                if (!btn) return;
                window.addEventListener('scroll', function() {
                  if (window.scrollY > 300) {
                    btn.classList.add('visible');
                  } else {
                    btn.classList.remove('visible');
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
