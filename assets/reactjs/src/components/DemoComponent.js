import React from "react";
import { useEffect } from "react";

function DemoComponent(props) {
  useEffect(() => {
    console.log('useEffect')
  }, []);

    return (
      <div>
        <h2>Demo Component</h2>
      </div>
    );
}

export default DemoComponent;
