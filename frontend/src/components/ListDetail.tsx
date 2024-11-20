import { useParams } from "react-router-dom";

export default function ListDetail() {
    const { slug } = useParams();
    return <div>Detail for slug: {slug}</div>;
}