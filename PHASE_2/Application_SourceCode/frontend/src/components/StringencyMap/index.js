import React, { useState } from "react";
import ReactDOM from "react-dom";
import ReactTooltip from "react-tooltip";

// import "./styles.css";

import StringencyMap from "./StringencyMap";

function App() {
  const [content, setContent] = useState("");
  return (
    <div>
      <StringencyMap setTooltipContent={setContent} />
      <ReactTooltip>{content}</ReactTooltip>
    </div>
  );
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);
