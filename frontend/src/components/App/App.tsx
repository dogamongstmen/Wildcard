import { CardPreview } from "../CardPreview/CardPreview";
import "./app.css";

export function App(): JSX.Element {
  return <span className="background">
    <CardPreview
      cardSet={{ name: "Elementary music theory", id: "1234567890", cover_img: null }}
      skeleton={true} />
  </span>
}