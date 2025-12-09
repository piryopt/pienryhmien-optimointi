import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import "../static/css/markdown.css";
const MarkdownRenderer = ({ srcPath, content }) => {
  const [md, setMd] = useState("");

  useEffect(() => {
    let mounted = true;
    if (typeof content === "string" && content.length > 0) {
      setMd(content);
      return () => (mounted = false);
    }
    if (!srcPath) {
      setMd("");
      return () => (mounted = false);
    }
    fetch(srcPath)
      .then((r) => r.text())
      .then((text) => {
        if (mounted) setMd(text);
      })
      .catch(() => {
        if (mounted) setMd("Virhe ladattaessa sisältöä.");
      });
    return () => (mounted = false);
  }, [srcPath, content]);

  return (
    <div className="markdown-content">
      <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeRaw]}>
        {md}
      </ReactMarkdown>
    </div>
  );
};

export default MarkdownRenderer;
