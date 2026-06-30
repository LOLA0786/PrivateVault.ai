import { Link } from 'react-router-dom';
import { posts } from './posts';
import './blog.css';
const fmt = (d) => (d ? new Date(d).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }) : '');
export default function Blog() {
  return (
    <main className="pv-blog">
      <header className="pv-blog__head">
        <p className="pv-blog__eyebrow">PrivateVault / Perspective</p>
        <h1>Decision Integrity for Regulated AI</h1>
        <p className="pv-blog__sub">Notes on governing autonomous decisions in regulated industries: credit, payments, claims.</p>
      </header>
      <ul className="pv-blog__list">
        {posts.map((p) => (
          <li key={p.slug} className="pv-blog__item">
            <Link to={`/blog/${p.slug}`}>
              <span className="pv-blog__date">{fmt(p.date)}</span>
              <h2>{p.title}</h2>
              <p>{p.excerpt}</p>
            </Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
