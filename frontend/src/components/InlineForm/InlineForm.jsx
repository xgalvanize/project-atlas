import { useState } from "react";
import ui from "../../styles/ui.module.css";
import styles from "./InlineForm.module.css";

export default function InlineForm({
  placeholder,
  buttonText,
  onSubmit,
}) {
  const [value, setValue] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    if (!value.trim()) return;

    await onSubmit(value);
    setValue("");
  }

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <input
        className={ui.input}
        value={value}
        placeholder={placeholder}
        onChange={(e) => setValue(e.target.value)}
      />

      <button className={`${ui.button} ${ui.buttonPrimary}`}>
        {buttonText}
      </button>
    </form>
  );
}
