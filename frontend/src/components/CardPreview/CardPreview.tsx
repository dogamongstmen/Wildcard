import { CardSet } from "../../modules/types/api/CardSet";
import { Button } from "../Button/Button";
import "./cardpreview.css";

export function CardPreview(props: { cardSet: CardSet, skeleton: boolean }): JSX.Element {
  return <span className={props.skeleton ? "card-preview-bg" : "card-preview-bg"}>
    <span className="card-preview-thumb"></span>
    <span className="text no-select card-preview-label">{props.cardSet.name}</span>
    <Button className="card-preview-btn" label="Study" />
  </span>
}