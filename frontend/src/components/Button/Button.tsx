import "./button.css";

export function Button(props: { label: string, className: string }): JSX.Element {
  return <button className={`text button-base ${props.className}`}>{props.label}</button>
}