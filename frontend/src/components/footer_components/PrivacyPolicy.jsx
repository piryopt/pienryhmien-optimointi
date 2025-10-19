import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";

const PRIVACY_POLICY_PATH = "/content/Tietosuojaseloste.md";

const PrivacyPolicy = () => {
  const [markdown, setMarkdown] = useState("");

  useEffect(() => {
    fetch(PRIVACY_POLICY_PATH)
      .then((res) => res.text())
      .then(setMarkdown);
  }, []);

  return (
    <div className="container">
      <ReactMarkdown>{markdown}</ReactMarkdown>
    </div>
  );
};

export default PrivacyPolicy;
