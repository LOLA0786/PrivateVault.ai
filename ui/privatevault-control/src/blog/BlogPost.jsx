import { useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { getPost } from './posts';
import './blog.css';
const fmt = (d) => (d ? new Date(d).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }) : '');
function setMeta(name, content) {
  let el = document.querySelector(`meta[name="${name}"]`);
  if (!el) { el = document.createElement('meta'); el.setAttribute('name', name); document.head.appendChild(el); }
  el.setAttribute('content', content || '');
}
export default function BlogPost() {
  const { slug } = useParams();
  const post = getPost(slug);
  useEffect(() => {
    if (!post) return;
    document.title = `${post.title} | PrivateVault`;
    setMeta('description', post.excerpt);
  }, [post]);
  if (!post) {
    return (<main className="pv-blog"><p>Post not found. <Link to="/blog">Back to all posts</Link></p></main>);
  }
  return (
    <main className="pv-blog pv-blog--post">
      <Link className="pv-blog__back" to="/blog">All posts</Link>
      <article>
        <p className="pv-blog__date">{fmt(post.date)}</p>
        <h1>{post.title}</h1>
        <div className="pv-blog__body"><ReactMarkdown remarkPlugins={[remarkGfm]}>{post.body}</ReactMarkdown></div>
      </article>
    </main>
  );
}
