import { readFileSync } from "fs";
import { join } from "path";
import type {
  QuartzComponent,
  QuartzComponentConstructor,
  QuartzComponentProps,
} from "./types";

function getQuartzVersion(): string {
  try {
    const pkg = JSON.parse(readFileSync(join(process.cwd(), "package.json"), "utf-8"));
    return pkg.version ?? "";
  } catch {
    return "";
  }
}

export interface FooterOptions {
  links?: Record<string, string>;
}

const defaultLinks: Record<string, string> = {
  "CC BY-NC-SA 4.0": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
  "免责声明": "/02-帮助/免责声明",
  "联系我们": "/02-帮助/联系我们",
  "关于本站": "/02-帮助/关于",
  "常见问答": "/02-帮助/常见问答",
};

export default ((opts?: FooterOptions) => {
  const version = getQuartzVersion();

  const Footer: QuartzComponent = ({ displayClass }: QuartzComponentProps) => {
    const year = new Date().getFullYear();
    const links = opts?.links ?? defaultLinks;

    return (
      <footer class={displayClass ?? ""} style="text-align:left;margin-bottom:4rem;opacity:0.7;line-height:1.6;font-size:0.9rem">
        <div style="margin-bottom:0.5rem">
          Created with Quartz v{version} © {year}
        </div>
        <div style="margin-bottom:0.5rem">
          本站内容除特别说明外，均在{" "}
          <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank" rel="noopener noreferrer" style="color:var(--secondary)">
            CC BY-NC-SA 4.0
          </a>{" "}
          协议下提供，附加条款亦可能应用
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;gap:1rem">
          <ul style="list-style:none;margin:0;padding:0;display:flex;gap:1rem;flex-wrap:wrap">
            {Object.entries(links).map(([text, link]) => (
              <li key={text}>
                <a href={link} style="color:var(--secondary);text-decoration:none">{text}</a>
              </li>
            ))}
          </ul>
          <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank" rel="noopener noreferrer" style="flex-shrink:0">
            <img src="https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png" alt="CC BY-NC-SA 4.0" style="display:block;border:none;height:31px;width:auto" />
          </a>
        </div>
      </footer>
    );
  };

  return Footer;
}) satisfies QuartzComponentConstructor;
