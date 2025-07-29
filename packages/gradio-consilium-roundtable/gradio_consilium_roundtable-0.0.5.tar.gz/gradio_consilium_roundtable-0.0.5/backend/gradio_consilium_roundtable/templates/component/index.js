var st = Object.defineProperty;
var ve = (r) => {
  throw TypeError(r);
};
var it = (r, e, t) => e in r ? st(r, e, { enumerable: !0, configurable: !0, writable: !0, value: t }) : r[e] = t;
var x = (r, e, t) => it(r, typeof e != "symbol" ? e + "" : e, t), lt = (r, e, t) => e.has(r) || ve("Cannot " + t);
var Te = (r, e, t) => e.has(r) ? ve("Cannot add the same private member more than once") : e instanceof WeakSet ? e.add(r) : e.set(r, t);
var ee = (r, e, t) => (lt(r, e, "access private method"), t);
function fe() {
  return {
    async: !1,
    breaks: !1,
    extensions: null,
    gfm: !0,
    hooks: null,
    pedantic: !1,
    renderer: null,
    silent: !1,
    tokenizer: null,
    walkTokens: null
  };
}
let O = fe();
function qe(r) {
  O = r;
}
const De = /[&<>"']/, rt = new RegExp(De.source, "g"), Ze = /[<>"']|&(?!(#\d{1,7}|#[Xx][a-fA-F0-9]{1,6}|\w+);)/, ot = new RegExp(Ze.source, "g"), at = {
  "&": "&amp;",
  "<": "&lt;",
  ">": "&gt;",
  '"': "&quot;",
  "'": "&#39;"
}, ze = (r) => at[r];
function C(r, e) {
  if (e) {
    if (De.test(r))
      return r.replace(rt, ze);
  } else if (Ze.test(r))
    return r.replace(ot, ze);
  return r;
}
const ct = /&(#(?:\d+)|(?:#x[0-9A-Fa-f]+)|(?:\w+));?/ig;
function ht(r) {
  return r.replace(ct, (e, t) => (t = t.toLowerCase(), t === "colon" ? ":" : t.charAt(0) === "#" ? t.charAt(1) === "x" ? String.fromCharCode(parseInt(t.substring(2), 16)) : String.fromCharCode(+t.substring(1)) : ""));
}
const ut = /(^|[^\[])\^/g;
function w(r, e) {
  let t = typeof r == "string" ? r : r.source;
  e = e || "";
  const n = {
    replace: (i, l) => {
      let s = typeof l == "string" ? l : l.source;
      return s = s.replace(ut, "$1"), t = t.replace(i, s), n;
    },
    getRegex: () => new RegExp(t, e)
  };
  return n;
}
function Ie(r) {
  try {
    r = encodeURI(r).replace(/%25/g, "%");
  } catch {
    return null;
  }
  return r;
}
const F = { exec: () => null };
function Re(r, e) {
  const t = r.replace(/\|/g, (l, s, o) => {
    let a = !1, u = s;
    for (; --u >= 0 && o[u] === "\\"; )
      a = !a;
    return a ? "|" : " |";
  }), n = t.split(/ \|/);
  let i = 0;
  if (n[0].trim() || n.shift(), n.length > 0 && !n[n.length - 1].trim() && n.pop(), e)
    if (n.length > e)
      n.splice(e);
    else
      for (; n.length < e; )
        n.push("");
  for (; i < n.length; i++)
    n[i] = n[i].trim().replace(/\\\|/g, "|");
  return n;
}
function te(r, e, t) {
  const n = r.length;
  if (n === 0)
    return "";
  let i = 0;
  for (; i < n && r.charAt(n - i - 1) === e; )
    i++;
  return r.slice(0, n - i);
}
function pt(r, e) {
  if (r.indexOf(e[1]) === -1)
    return -1;
  let t = 0;
  for (let n = 0; n < r.length; n++)
    if (r[n] === "\\")
      n++;
    else if (r[n] === e[0])
      t++;
    else if (r[n] === e[1] && (t--, t < 0))
      return n;
  return -1;
}
function Se(r, e, t, n) {
  const i = e.href, l = e.title ? C(e.title) : null, s = r[1].replace(/\\([\[\]])/g, "$1");
  if (r[0].charAt(0) !== "!") {
    n.state.inLink = !0;
    const o = {
      type: "link",
      raw: t,
      href: i,
      title: l,
      text: s,
      tokens: n.inlineTokens(s)
    };
    return n.state.inLink = !1, o;
  }
  return {
    type: "image",
    raw: t,
    href: i,
    title: l,
    text: C(s)
  };
}
function ft(r, e) {
  const t = r.match(/^(\s+)(?:```)/);
  if (t === null)
    return e;
  const n = t[1];
  return e.split(`
`).map((i) => {
    const l = i.match(/^\s+/);
    if (l === null)
      return i;
    const [s] = l;
    return s.length >= n.length ? i.slice(n.length) : i;
  }).join(`
`);
}
class se {
  // set by the lexer
  constructor(e) {
    x(this, "options");
    x(this, "rules");
    // set by the lexer
    x(this, "lexer");
    this.options = e || O;
  }
  space(e) {
    const t = this.rules.block.newline.exec(e);
    if (t && t[0].length > 0)
      return {
        type: "space",
        raw: t[0]
      };
  }
  code(e) {
    const t = this.rules.block.code.exec(e);
    if (t) {
      const n = t[0].replace(/^ {1,4}/gm, "");
      return {
        type: "code",
        raw: t[0],
        codeBlockStyle: "indented",
        text: this.options.pedantic ? n : te(n, `
`)
      };
    }
  }
  fences(e) {
    const t = this.rules.block.fences.exec(e);
    if (t) {
      const n = t[0], i = ft(n, t[3] || "");
      return {
        type: "code",
        raw: n,
        lang: t[2] ? t[2].trim().replace(this.rules.inline.anyPunctuation, "$1") : t[2],
        text: i
      };
    }
  }
  heading(e) {
    const t = this.rules.block.heading.exec(e);
    if (t) {
      let n = t[2].trim();
      if (/#$/.test(n)) {
        const i = te(n, "#");
        (this.options.pedantic || !i || / $/.test(i)) && (n = i.trim());
      }
      return {
        type: "heading",
        raw: t[0],
        depth: t[1].length,
        text: n,
        tokens: this.lexer.inline(n)
      };
    }
  }
  hr(e) {
    const t = this.rules.block.hr.exec(e);
    if (t)
      return {
        type: "hr",
        raw: t[0]
      };
  }
  blockquote(e) {
    const t = this.rules.block.blockquote.exec(e);
    if (t) {
      let n = t[0].replace(/\n {0,3}((?:=+|-+) *)(?=\n|$)/g, `
    $1`);
      n = te(n.replace(/^ *>[ \t]?/gm, ""), `
`);
      const i = this.lexer.state.top;
      this.lexer.state.top = !0;
      const l = this.lexer.blockTokens(n);
      return this.lexer.state.top = i, {
        type: "blockquote",
        raw: t[0],
        tokens: l,
        text: n
      };
    }
  }
  list(e) {
    let t = this.rules.block.list.exec(e);
    if (t) {
      let n = t[1].trim();
      const i = n.length > 1, l = {
        type: "list",
        raw: "",
        ordered: i,
        start: i ? +n.slice(0, -1) : "",
        loose: !1,
        items: []
      };
      n = i ? `\\d{1,9}\\${n.slice(-1)}` : `\\${n}`, this.options.pedantic && (n = i ? n : "[*+-]");
      const s = new RegExp(`^( {0,3}${n})((?:[	 ][^\\n]*)?(?:\\n|$))`);
      let o = "", a = "", u = !1;
      for (; e; ) {
        let c = !1;
        if (!(t = s.exec(e)) || this.rules.block.hr.test(e))
          break;
        o = t[0], e = e.substring(o.length);
        let h = t[2].split(`
`, 1)[0].replace(/^\t+/, ($) => " ".repeat(3 * $.length)), p = e.split(`
`, 1)[0], g = 0;
        this.options.pedantic ? (g = 2, a = h.trimStart()) : (g = t[2].search(/[^ ]/), g = g > 4 ? 1 : g, a = h.slice(g), g += t[1].length);
        let _ = !1;
        if (!h && /^ *$/.test(p) && (o += p + `
`, e = e.substring(p.length + 1), c = !0), !c) {
          const $ = new RegExp(`^ {0,${Math.min(3, g - 1)}}(?:[*+-]|\\d{1,9}[.)])((?:[ 	][^\\n]*)?(?:\\n|$))`), T = new RegExp(`^ {0,${Math.min(3, g - 1)}}((?:- *){3,}|(?:_ *){3,}|(?:\\* *){3,})(?:\\n+|$)`), d = new RegExp(`^ {0,${Math.min(3, g - 1)}}(?:\`\`\`|~~~)`), m = new RegExp(`^ {0,${Math.min(3, g - 1)}}#`);
          for (; e; ) {
            const R = e.split(`
`, 1)[0];
            if (p = R, this.options.pedantic && (p = p.replace(/^ {1,4}(?=( {4})*[^ ])/g, "  ")), d.test(p) || m.test(p) || $.test(p) || T.test(e))
              break;
            if (p.search(/[^ ]/) >= g || !p.trim())
              a += `
` + p.slice(g);
            else {
              if (_ || h.search(/[^ ]/) >= 4 || d.test(h) || m.test(h) || T.test(h))
                break;
              a += `
` + p;
            }
            !_ && !p.trim() && (_ = !0), o += R + `
`, e = e.substring(R.length + 1), h = p.slice(g);
          }
        }
        l.loose || (u ? l.loose = !0 : /\n *\n *$/.test(o) && (u = !0));
        let y = null, z;
        this.options.gfm && (y = /^\[[ xX]\] /.exec(a), y && (z = y[0] !== "[ ] ", a = a.replace(/^\[[ xX]\] +/, ""))), l.items.push({
          type: "list_item",
          raw: o,
          task: !!y,
          checked: z,
          loose: !1,
          text: a,
          tokens: []
        }), l.raw += o;
      }
      l.items[l.items.length - 1].raw = o.trimEnd(), l.items[l.items.length - 1].text = a.trimEnd(), l.raw = l.raw.trimEnd();
      for (let c = 0; c < l.items.length; c++)
        if (this.lexer.state.top = !1, l.items[c].tokens = this.lexer.blockTokens(l.items[c].text, []), !l.loose) {
          const h = l.items[c].tokens.filter((g) => g.type === "space"), p = h.length > 0 && h.some((g) => /\n.*\n/.test(g.raw));
          l.loose = p;
        }
      if (l.loose)
        for (let c = 0; c < l.items.length; c++)
          l.items[c].loose = !0;
      return l;
    }
  }
  html(e) {
    const t = this.rules.block.html.exec(e);
    if (t)
      return {
        type: "html",
        block: !0,
        raw: t[0],
        pre: t[1] === "pre" || t[1] === "script" || t[1] === "style",
        text: t[0]
      };
  }
  def(e) {
    const t = this.rules.block.def.exec(e);
    if (t) {
      const n = t[1].toLowerCase().replace(/\s+/g, " "), i = t[2] ? t[2].replace(/^<(.*)>$/, "$1").replace(this.rules.inline.anyPunctuation, "$1") : "", l = t[3] ? t[3].substring(1, t[3].length - 1).replace(this.rules.inline.anyPunctuation, "$1") : t[3];
      return {
        type: "def",
        tag: n,
        raw: t[0],
        href: i,
        title: l
      };
    }
  }
  table(e) {
    const t = this.rules.block.table.exec(e);
    if (!t || !/[:|]/.test(t[2]))
      return;
    const n = Re(t[1]), i = t[2].replace(/^\||\| *$/g, "").split("|"), l = t[3] && t[3].trim() ? t[3].replace(/\n[ \t]*$/, "").split(`
`) : [], s = {
      type: "table",
      raw: t[0],
      header: [],
      align: [],
      rows: []
    };
    if (n.length === i.length) {
      for (const o of i)
        /^ *-+: *$/.test(o) ? s.align.push("right") : /^ *:-+: *$/.test(o) ? s.align.push("center") : /^ *:-+ *$/.test(o) ? s.align.push("left") : s.align.push(null);
      for (const o of n)
        s.header.push({
          text: o,
          tokens: this.lexer.inline(o)
        });
      for (const o of l)
        s.rows.push(Re(o, s.header.length).map((a) => ({
          text: a,
          tokens: this.lexer.inline(a)
        })));
      return s;
    }
  }
  lheading(e) {
    const t = this.rules.block.lheading.exec(e);
    if (t)
      return {
        type: "heading",
        raw: t[0],
        depth: t[2].charAt(0) === "=" ? 1 : 2,
        text: t[1],
        tokens: this.lexer.inline(t[1])
      };
  }
  paragraph(e) {
    const t = this.rules.block.paragraph.exec(e);
    if (t) {
      const n = t[1].charAt(t[1].length - 1) === `
` ? t[1].slice(0, -1) : t[1];
      return {
        type: "paragraph",
        raw: t[0],
        text: n,
        tokens: this.lexer.inline(n)
      };
    }
  }
  text(e) {
    const t = this.rules.block.text.exec(e);
    if (t)
      return {
        type: "text",
        raw: t[0],
        text: t[0],
        tokens: this.lexer.inline(t[0])
      };
  }
  escape(e) {
    const t = this.rules.inline.escape.exec(e);
    if (t)
      return {
        type: "escape",
        raw: t[0],
        text: C(t[1])
      };
  }
  tag(e) {
    const t = this.rules.inline.tag.exec(e);
    if (t)
      return !this.lexer.state.inLink && /^<a /i.test(t[0]) ? this.lexer.state.inLink = !0 : this.lexer.state.inLink && /^<\/a>/i.test(t[0]) && (this.lexer.state.inLink = !1), !this.lexer.state.inRawBlock && /^<(pre|code|kbd|script)(\s|>)/i.test(t[0]) ? this.lexer.state.inRawBlock = !0 : this.lexer.state.inRawBlock && /^<\/(pre|code|kbd|script)(\s|>)/i.test(t[0]) && (this.lexer.state.inRawBlock = !1), {
        type: "html",
        raw: t[0],
        inLink: this.lexer.state.inLink,
        inRawBlock: this.lexer.state.inRawBlock,
        block: !1,
        text: t[0]
      };
  }
  link(e) {
    const t = this.rules.inline.link.exec(e);
    if (t) {
      const n = t[2].trim();
      if (!this.options.pedantic && /^</.test(n)) {
        if (!/>$/.test(n))
          return;
        const s = te(n.slice(0, -1), "\\");
        if ((n.length - s.length) % 2 === 0)
          return;
      } else {
        const s = pt(t[2], "()");
        if (s > -1) {
          const a = (t[0].indexOf("!") === 0 ? 5 : 4) + t[1].length + s;
          t[2] = t[2].substring(0, s), t[0] = t[0].substring(0, a).trim(), t[3] = "";
        }
      }
      let i = t[2], l = "";
      if (this.options.pedantic) {
        const s = /^([^'"]*[^\s])\s+(['"])(.*)\2/.exec(i);
        s && (i = s[1], l = s[3]);
      } else
        l = t[3] ? t[3].slice(1, -1) : "";
      return i = i.trim(), /^</.test(i) && (this.options.pedantic && !/>$/.test(n) ? i = i.slice(1) : i = i.slice(1, -1)), Se(t, {
        href: i && i.replace(this.rules.inline.anyPunctuation, "$1"),
        title: l && l.replace(this.rules.inline.anyPunctuation, "$1")
      }, t[0], this.lexer);
    }
  }
  reflink(e, t) {
    let n;
    if ((n = this.rules.inline.reflink.exec(e)) || (n = this.rules.inline.nolink.exec(e))) {
      const i = (n[2] || n[1]).replace(/\s+/g, " "), l = t[i.toLowerCase()];
      if (!l) {
        const s = n[0].charAt(0);
        return {
          type: "text",
          raw: s,
          text: s
        };
      }
      return Se(n, l, n[0], this.lexer);
    }
  }
  emStrong(e, t, n = "") {
    let i = this.rules.inline.emStrongLDelim.exec(e);
    if (!i || i[3] && n.match(/[\p{L}\p{N}]/u))
      return;
    if (!(i[1] || i[2] || "") || !n || this.rules.inline.punctuation.exec(n)) {
      const s = [...i[0]].length - 1;
      let o, a, u = s, c = 0;
      const h = i[0][0] === "*" ? this.rules.inline.emStrongRDelimAst : this.rules.inline.emStrongRDelimUnd;
      for (h.lastIndex = 0, t = t.slice(-1 * e.length + s); (i = h.exec(t)) != null; ) {
        if (o = i[1] || i[2] || i[3] || i[4] || i[5] || i[6], !o)
          continue;
        if (a = [...o].length, i[3] || i[4]) {
          u += a;
          continue;
        } else if ((i[5] || i[6]) && s % 3 && !((s + a) % 3)) {
          c += a;
          continue;
        }
        if (u -= a, u > 0)
          continue;
        a = Math.min(a, a + u + c);
        const p = [...i[0]][0].length, g = e.slice(0, s + i.index + p + a);
        if (Math.min(s, a) % 2) {
          const y = g.slice(1, -1);
          return {
            type: "em",
            raw: g,
            text: y,
            tokens: this.lexer.inlineTokens(y)
          };
        }
        const _ = g.slice(2, -2);
        return {
          type: "strong",
          raw: g,
          text: _,
          tokens: this.lexer.inlineTokens(_)
        };
      }
    }
  }
  codespan(e) {
    const t = this.rules.inline.code.exec(e);
    if (t) {
      let n = t[2].replace(/\n/g, " ");
      const i = /[^ ]/.test(n), l = /^ /.test(n) && / $/.test(n);
      return i && l && (n = n.substring(1, n.length - 1)), n = C(n, !0), {
        type: "codespan",
        raw: t[0],
        text: n
      };
    }
  }
  br(e) {
    const t = this.rules.inline.br.exec(e);
    if (t)
      return {
        type: "br",
        raw: t[0]
      };
  }
  del(e) {
    const t = this.rules.inline.del.exec(e);
    if (t)
      return {
        type: "del",
        raw: t[0],
        text: t[2],
        tokens: this.lexer.inlineTokens(t[2])
      };
  }
  autolink(e) {
    const t = this.rules.inline.autolink.exec(e);
    if (t) {
      let n, i;
      return t[2] === "@" ? (n = C(t[1]), i = "mailto:" + n) : (n = C(t[1]), i = n), {
        type: "link",
        raw: t[0],
        text: n,
        href: i,
        tokens: [
          {
            type: "text",
            raw: n,
            text: n
          }
        ]
      };
    }
  }
  url(e) {
    var n;
    let t;
    if (t = this.rules.inline.url.exec(e)) {
      let i, l;
      if (t[2] === "@")
        i = C(t[0]), l = "mailto:" + i;
      else {
        let s;
        do
          s = t[0], t[0] = ((n = this.rules.inline._backpedal.exec(t[0])) == null ? void 0 : n[0]) ?? "";
        while (s !== t[0]);
        i = C(t[0]), t[1] === "www." ? l = "http://" + t[0] : l = t[0];
      }
      return {
        type: "link",
        raw: t[0],
        text: i,
        href: l,
        tokens: [
          {
            type: "text",
            raw: i,
            text: i
          }
        ]
      };
    }
  }
  inlineText(e) {
    const t = this.rules.inline.text.exec(e);
    if (t) {
      let n;
      return this.lexer.state.inRawBlock ? n = t[0] : n = C(t[0]), {
        type: "text",
        raw: t[0],
        text: n
      };
    }
  }
}
const gt = /^(?: *(?:\n|$))+/, dt = /^( {4}[^\n]+(?:\n(?: *(?:\n|$))*)?)+/, kt = /^ {0,3}(`{3,}(?=[^`\n]*(?:\n|$))|~{3,})([^\n]*)(?:\n|$)(?:|([\s\S]*?)(?:\n|$))(?: {0,3}\1[~`]* *(?=\n|$)|$)/, U = /^ {0,3}((?:-[\t ]*){3,}|(?:_[ \t]*){3,}|(?:\*[ \t]*){3,})(?:\n+|$)/, mt = /^ {0,3}(#{1,6})(?=\s|$)(.*)(?:\n+|$)/, Oe = /(?:[*+-]|\d{1,9}[.)])/, je = w(/^(?!bull |blockCode|fences|blockquote|heading|html)((?:.|\n(?!\s*?\n|bull |blockCode|fences|blockquote|heading|html))+?)\n {0,3}(=+|-+) *(?:\n+|$)/).replace(/bull/g, Oe).replace(/blockCode/g, / {4}/).replace(/fences/g, / {0,3}(?:`{3,}|~{3,})/).replace(/blockquote/g, / {0,3}>/).replace(/heading/g, / {0,3}#{1,6}/).replace(/html/g, / {0,3}<[^\n>]+>\n/).getRegex(), ge = /^([^\n]+(?:\n(?!hr|heading|lheading|blockquote|fences|list|html|table| +\n)[^\n]+)*)/, bt = /^[^\n]+/, de = /(?!\s*\])(?:\\.|[^\[\]\\])+/, wt = w(/^ {0,3}\[(label)\]: *(?:\n *)?([^<\s][^\s]*|<.*?>)(?:(?: +(?:\n *)?| *\n *)(title))? *(?:\n+|$)/).replace("label", de).replace("title", /(?:"(?:\\"?|[^"\\])*"|'[^'\n]*(?:\n[^'\n]+)*\n?'|\([^()]*\))/).getRegex(), xt = w(/^( {0,3}bull)([ \t][^\n]+?)?(?:\n|$)/).replace(/bull/g, Oe).getRegex(), oe = "address|article|aside|base|basefont|blockquote|body|caption|center|col|colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|footer|form|frame|frameset|h[1-6]|head|header|hr|html|iframe|legend|li|link|main|menu|menuitem|meta|nav|noframes|ol|optgroup|option|p|param|search|section|summary|table|tbody|td|tfoot|th|thead|title|tr|track|ul", ke = /<!--(?:-?>|[\s\S]*?(?:-->|$))/, _t = w("^ {0,3}(?:<(script|pre|style|textarea)[\\s>][\\s\\S]*?(?:</\\1>[^\\n]*\\n+|$)|comment[^\\n]*(\\n+|$)|<\\?[\\s\\S]*?(?:\\?>\\n*|$)|<![A-Z][\\s\\S]*?(?:>\\n*|$)|<!\\[CDATA\\[[\\s\\S]*?(?:\\]\\]>\\n*|$)|</?(tag)(?: +|\\n|/?>)[\\s\\S]*?(?:(?:\\n *)+\\n|$)|<(?!script|pre|style|textarea)([a-z][\\w-]*)(?:attribute)*? */?>(?=[ \\t]*(?:\\n|$))[\\s\\S]*?(?:(?:\\n *)+\\n|$)|</(?!script|pre|style|textarea)[a-z][\\w-]*\\s*>(?=[ \\t]*(?:\\n|$))[\\s\\S]*?(?:(?:\\n *)+\\n|$))", "i").replace("comment", ke).replace("tag", oe).replace("attribute", / +[a-zA-Z:_][\w.:-]*(?: *= *"[^"\n]*"| *= *'[^'\n]*'| *= *[^\s"'=<>`]+)?/).getRegex(), Qe = w(ge).replace("hr", U).replace("heading", " {0,3}#{1,6}(?:\\s|$)").replace("|lheading", "").replace("|table", "").replace("blockquote", " {0,3}>").replace("fences", " {0,3}(?:`{3,}(?=[^`\\n]*\\n)|~{3,})[^\\n]*\\n").replace("list", " {0,3}(?:[*+-]|1[.)]) ").replace("html", "</?(?:tag)(?: +|\\n|/?>)|<(?:script|pre|style|textarea|!--)").replace("tag", oe).getRegex(), yt = w(/^( {0,3}> ?(paragraph|[^\n]*)(?:\n|$))+/).replace("paragraph", Qe).getRegex(), me = {
  blockquote: yt,
  code: dt,
  def: wt,
  fences: kt,
  heading: mt,
  hr: U,
  html: _t,
  lheading: je,
  list: xt,
  newline: gt,
  paragraph: Qe,
  table: F,
  text: bt
}, Ae = w("^ *([^\\n ].*)\\n {0,3}((?:\\| *)?:?-+:? *(?:\\| *:?-+:? *)*(?:\\| *)?)(?:\\n((?:(?! *\\n|hr|heading|blockquote|code|fences|list|html).*(?:\\n|$))*)\\n*|$)").replace("hr", U).replace("heading", " {0,3}#{1,6}(?:\\s|$)").replace("blockquote", " {0,3}>").replace("code", " {4}[^\\n]").replace("fences", " {0,3}(?:`{3,}(?=[^`\\n]*\\n)|~{3,})[^\\n]*\\n").replace("list", " {0,3}(?:[*+-]|1[.)]) ").replace("html", "</?(?:tag)(?: +|\\n|/?>)|<(?:script|pre|style|textarea|!--)").replace("tag", oe).getRegex(), vt = {
  ...me,
  table: Ae,
  paragraph: w(ge).replace("hr", U).replace("heading", " {0,3}#{1,6}(?:\\s|$)").replace("|lheading", "").replace("table", Ae).replace("blockquote", " {0,3}>").replace("fences", " {0,3}(?:`{3,}(?=[^`\\n]*\\n)|~{3,})[^\\n]*\\n").replace("list", " {0,3}(?:[*+-]|1[.)]) ").replace("html", "</?(?:tag)(?: +|\\n|/?>)|<(?:script|pre|style|textarea|!--)").replace("tag", oe).getRegex()
}, Tt = {
  ...me,
  html: w(`^ *(?:comment *(?:\\n|\\s*$)|<(tag)[\\s\\S]+?</\\1> *(?:\\n{2,}|\\s*$)|<tag(?:"[^"]*"|'[^']*'|\\s[^'"/>\\s]*)*?/?> *(?:\\n{2,}|\\s*$))`).replace("comment", ke).replace(/tag/g, "(?!(?:a|em|strong|small|s|cite|q|dfn|abbr|data|time|code|var|samp|kbd|sub|sup|i|b|u|mark|ruby|rt|rp|bdi|bdo|span|br|wbr|ins|del|img)\\b)\\w+(?!:|[^\\w\\s@]*@)\\b").getRegex(),
  def: /^ *\[([^\]]+)\]: *<?([^\s>]+)>?(?: +(["(][^\n]+[")]))? *(?:\n+|$)/,
  heading: /^(#{1,6})(.*)(?:\n+|$)/,
  fences: F,
  // fences not supported
  lheading: /^(.+?)\n {0,3}(=+|-+) *(?:\n+|$)/,
  paragraph: w(ge).replace("hr", U).replace("heading", ` *#{1,6} *[^
]`).replace("lheading", je).replace("|table", "").replace("blockquote", " {0,3}>").replace("|fences", "").replace("|list", "").replace("|html", "").replace("|tag", "").getRegex()
}, Ve = /^\\([!"#$%&'()*+,\-./:;<=>?@\[\]\\^_`{|}~])/, zt = /^(`+)([^`]|[^`][\s\S]*?[^`])\1(?!`)/, Ne = /^( {2,}|\\)\n(?!\s*$)/, It = /^(`+|[^`])(?:(?= {2,}\n)|[\s\S]*?(?:(?=[\\<!\[`*_]|\b_|$)|[^ ](?= {2,}\n)))/, W = "\\p{P}\\p{S}", Rt = w(/^((?![*_])[\spunctuation])/, "u").replace(/punctuation/g, W).getRegex(), St = /\[[^[\]]*?\]\([^\(\)]*?\)|`[^`]*?`|<[^<>]*?>/g, At = w(/^(?:\*+(?:((?!\*)[punct])|[^\s*]))|^_+(?:((?!_)[punct])|([^\s_]))/, "u").replace(/punct/g, W).getRegex(), Et = w("^[^_*]*?__[^_*]*?\\*[^_*]*?(?=__)|[^*]+(?=[^*])|(?!\\*)[punct](\\*+)(?=[\\s]|$)|[^punct\\s](\\*+)(?!\\*)(?=[punct\\s]|$)|(?!\\*)[punct\\s](\\*+)(?=[^punct\\s])|[\\s](\\*+)(?!\\*)(?=[punct])|(?!\\*)[punct](\\*+)(?!\\*)(?=[punct])|[^punct\\s](\\*+)(?=[^punct\\s])", "gu").replace(/punct/g, W).getRegex(), Lt = w("^[^_*]*?\\*\\*[^_*]*?_[^_*]*?(?=\\*\\*)|[^_]+(?=[^_])|(?!_)[punct](_+)(?=[\\s]|$)|[^punct\\s](_+)(?!_)(?=[punct\\s]|$)|(?!_)[punct\\s](_+)(?=[^punct\\s])|[\\s](_+)(?!_)(?=[punct])|(?!_)[punct](_+)(?!_)(?=[punct])", "gu").replace(/punct/g, W).getRegex(), Ct = w(/\\([punct])/, "gu").replace(/punct/g, W).getRegex(), $t = w(/^<(scheme:[^\s\x00-\x1f<>]*|email)>/).replace("scheme", /[a-zA-Z][a-zA-Z0-9+.-]{1,31}/).replace("email", /[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+(@)[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+(?![-_])/).getRegex(), Bt = w(ke).replace("(?:-->|$)", "-->").getRegex(), Mt = w("^comment|^</[a-zA-Z][\\w:-]*\\s*>|^<[a-zA-Z][\\w-]*(?:attribute)*?\\s*/?>|^<\\?[\\s\\S]*?\\?>|^<![a-zA-Z]+\\s[\\s\\S]*?>|^<!\\[CDATA\\[[\\s\\S]*?\\]\\]>").replace("comment", Bt).replace("attribute", /\s+[a-zA-Z:_][\w.:-]*(?:\s*=\s*"[^"]*"|\s*=\s*'[^']*'|\s*=\s*[^\s"'=<>`]+)?/).getRegex(), ie = /(?:\[(?:\\.|[^\[\]\\])*\]|\\.|`[^`]*`|[^\[\]\\`])*?/, Pt = w(/^!?\[(label)\]\(\s*(href)(?:\s+(title))?\s*\)/).replace("label", ie).replace("href", /<(?:\\.|[^\n<>\\])+>|[^\s\x00-\x1f]*/).replace("title", /"(?:\\"?|[^"\\])*"|'(?:\\'?|[^'\\])*'|\((?:\\\)?|[^)\\])*\)/).getRegex(), He = w(/^!?\[(label)\]\[(ref)\]/).replace("label", ie).replace("ref", de).getRegex(), Fe = w(/^!?\[(ref)\](?:\[\])?/).replace("ref", de).getRegex(), qt = w("reflink|nolink(?!\\()", "g").replace("reflink", He).replace("nolink", Fe).getRegex(), be = {
  _backpedal: F,
  // only used for GFM url
  anyPunctuation: Ct,
  autolink: $t,
  blockSkip: St,
  br: Ne,
  code: zt,
  del: F,
  emStrongLDelim: At,
  emStrongRDelimAst: Et,
  emStrongRDelimUnd: Lt,
  escape: Ve,
  link: Pt,
  nolink: Fe,
  punctuation: Rt,
  reflink: He,
  reflinkSearch: qt,
  tag: Mt,
  text: It,
  url: F
}, Dt = {
  ...be,
  link: w(/^!?\[(label)\]\((.*?)\)/).replace("label", ie).getRegex(),
  reflink: w(/^!?\[(label)\]\s*\[([^\]]*)\]/).replace("label", ie).getRegex()
}, ue = {
  ...be,
  escape: w(Ve).replace("])", "~|])").getRegex(),
  url: w(/^((?:ftp|https?):\/\/|www\.)(?:[a-zA-Z0-9\-]+\.?)+[^\s<]*|^email/, "i").replace("email", /[A-Za-z0-9._+-]+(@)[a-zA-Z0-9-_]+(?:\.[a-zA-Z0-9-_]*[a-zA-Z0-9])+(?![-_])/).getRegex(),
  _backpedal: /(?:[^?!.,:;*_'"~()&]+|\([^)]*\)|&(?![a-zA-Z0-9]+;$)|[?!.,:;*_'"~)]+(?!$))+/,
  del: /^(~~?)(?=[^\s~])([\s\S]*?[^\s~])\1(?=[^~]|$)/,
  text: /^([`~]+|[^`~])(?:(?= {2,}\n)|(?=[a-zA-Z0-9.!#$%&'*+\/=?_`{\|}~-]+@)|[\s\S]*?(?:(?=[\\<!\[`*~_]|\b_|https?:\/\/|ftp:\/\/|www\.|$)|[^ ](?= {2,}\n)|[^a-zA-Z0-9.!#$%&'*+\/=?_`{\|}~-](?=[a-zA-Z0-9.!#$%&'*+\/=?_`{\|}~-]+@)))/
}, Zt = {
  ...ue,
  br: w(Ne).replace("{2,}", "*").getRegex(),
  text: w(ue.text).replace("\\b_", "\\b_| {2,}\\n").replace(/\{2,\}/g, "*").getRegex()
}, ne = {
  normal: me,
  gfm: vt,
  pedantic: Tt
}, H = {
  normal: be,
  gfm: ue,
  breaks: Zt,
  pedantic: Dt
};
class M {
  constructor(e) {
    x(this, "tokens");
    x(this, "options");
    x(this, "state");
    x(this, "tokenizer");
    x(this, "inlineQueue");
    this.tokens = [], this.tokens.links = /* @__PURE__ */ Object.create(null), this.options = e || O, this.options.tokenizer = this.options.tokenizer || new se(), this.tokenizer = this.options.tokenizer, this.tokenizer.options = this.options, this.tokenizer.lexer = this, this.inlineQueue = [], this.state = {
      inLink: !1,
      inRawBlock: !1,
      top: !0
    };
    const t = {
      block: ne.normal,
      inline: H.normal
    };
    this.options.pedantic ? (t.block = ne.pedantic, t.inline = H.pedantic) : this.options.gfm && (t.block = ne.gfm, this.options.breaks ? t.inline = H.breaks : t.inline = H.gfm), this.tokenizer.rules = t;
  }
  /**
   * Expose Rules
   */
  static get rules() {
    return {
      block: ne,
      inline: H
    };
  }
  /**
   * Static Lex Method
   */
  static lex(e, t) {
    return new M(t).lex(e);
  }
  /**
   * Static Lex Inline Method
   */
  static lexInline(e, t) {
    return new M(t).inlineTokens(e);
  }
  /**
   * Preprocessing
   */
  lex(e) {
    e = e.replace(/\r\n|\r/g, `
`), this.blockTokens(e, this.tokens);
    for (let t = 0; t < this.inlineQueue.length; t++) {
      const n = this.inlineQueue[t];
      this.inlineTokens(n.src, n.tokens);
    }
    return this.inlineQueue = [], this.tokens;
  }
  blockTokens(e, t = []) {
    this.options.pedantic ? e = e.replace(/\t/g, "    ").replace(/^ +$/gm, "") : e = e.replace(/^( *)(\t+)/gm, (o, a, u) => a + "    ".repeat(u.length));
    let n, i, l, s;
    for (; e; )
      if (!(this.options.extensions && this.options.extensions.block && this.options.extensions.block.some((o) => (n = o.call({ lexer: this }, e, t)) ? (e = e.substring(n.raw.length), t.push(n), !0) : !1))) {
        if (n = this.tokenizer.space(e)) {
          e = e.substring(n.raw.length), n.raw.length === 1 && t.length > 0 ? t[t.length - 1].raw += `
` : t.push(n);
          continue;
        }
        if (n = this.tokenizer.code(e)) {
          e = e.substring(n.raw.length), i = t[t.length - 1], i && (i.type === "paragraph" || i.type === "text") ? (i.raw += `
` + n.raw, i.text += `
` + n.text, this.inlineQueue[this.inlineQueue.length - 1].src = i.text) : t.push(n);
          continue;
        }
        if (n = this.tokenizer.fences(e)) {
          e = e.substring(n.raw.length), t.push(n);
          continue;
        }
        if (n = this.tokenizer.heading(e)) {
          e = e.substring(n.raw.length), t.push(n);
          continue;
        }
        if (n = this.tokenizer.hr(e)) {
          e = e.substring(n.raw.length), t.push(n);
          continue;
        }
        if (n = this.tokenizer.blockquote(e)) {
          e = e.substring(n.raw.length), t.push(n);
          continue;
        }
        if (n = this.tokenizer.list(e)) {
          e = e.substring(n.raw.length), t.push(n);
          continue;
        }
        if (n = this.tokenizer.html(e)) {
          e = e.substring(n.raw.length), t.push(n);
          continue;
        }
        if (n = this.tokenizer.def(e)) {
          e = e.substring(n.raw.length), i = t[t.length - 1], i && (i.type === "paragraph" || i.type === "text") ? (i.raw += `
` + n.raw, i.text += `
` + n.raw, this.inlineQueue[this.inlineQueue.length - 1].src = i.text) : this.tokens.links[n.tag] || (this.tokens.links[n.tag] = {
            href: n.href,
            title: n.title
          });
          continue;
        }
        if (n = this.tokenizer.table(e)) {
          e = e.substring(n.raw.length), t.push(n);
          continue;
        }
        if (n = this.tokenizer.lheading(e)) {
          e = e.substring(n.raw.length), t.push(n);
          continue;
        }
        if (l = e, this.options.extensions && this.options.extensions.startBlock) {
          let o = 1 / 0;
          const a = e.slice(1);
          let u;
          this.options.extensions.startBlock.forEach((c) => {
            u = c.call({ lexer: this }, a), typeof u == "number" && u >= 0 && (o = Math.min(o, u));
          }), o < 1 / 0 && o >= 0 && (l = e.substring(0, o + 1));
        }
        if (this.state.top && (n = this.tokenizer.paragraph(l))) {
          i = t[t.length - 1], s && i.type === "paragraph" ? (i.raw += `
` + n.raw, i.text += `
` + n.text, this.inlineQueue.pop(), this.inlineQueue[this.inlineQueue.length - 1].src = i.text) : t.push(n), s = l.length !== e.length, e = e.substring(n.raw.length);
          continue;
        }
        if (n = this.tokenizer.text(e)) {
          e = e.substring(n.raw.length), i = t[t.length - 1], i && i.type === "text" ? (i.raw += `
` + n.raw, i.text += `
` + n.text, this.inlineQueue.pop(), this.inlineQueue[this.inlineQueue.length - 1].src = i.text) : t.push(n);
          continue;
        }
        if (e) {
          const o = "Infinite loop on byte: " + e.charCodeAt(0);
          if (this.options.silent) {
            console.error(o);
            break;
          } else
            throw new Error(o);
        }
      }
    return this.state.top = !0, t;
  }
  inline(e, t = []) {
    return this.inlineQueue.push({ src: e, tokens: t }), t;
  }
  /**
   * Lexing/Compiling
   */
  inlineTokens(e, t = []) {
    let n, i, l, s = e, o, a, u;
    if (this.tokens.links) {
      const c = Object.keys(this.tokens.links);
      if (c.length > 0)
        for (; (o = this.tokenizer.rules.inline.reflinkSearch.exec(s)) != null; )
          c.includes(o[0].slice(o[0].lastIndexOf("[") + 1, -1)) && (s = s.slice(0, o.index) + "[" + "a".repeat(o[0].length - 2) + "]" + s.slice(this.tokenizer.rules.inline.reflinkSearch.lastIndex));
    }
    for (; (o = this.tokenizer.rules.inline.blockSkip.exec(s)) != null; )
      s = s.slice(0, o.index) + "[" + "a".repeat(o[0].length - 2) + "]" + s.slice(this.tokenizer.rules.inline.blockSkip.lastIndex);
    for (; (o = this.tokenizer.rules.inline.anyPunctuation.exec(s)) != null; )
      s = s.slice(0, o.index) + "++" + s.slice(this.tokenizer.rules.inline.anyPunctuation.lastIndex);
    for (; e; )
      if (a || (u = ""), a = !1, !(this.options.extensions && this.options.extensions.inline && this.options.extensions.inline.some((c) => (n = c.call({ lexer: this }, e, t)) ? (e = e.substring(n.raw.length), t.push(n), !0) : !1))) {
        if (n = this.tokenizer.escape(e)) {
          e = e.substring(n.raw.length), t.push(n);
          continue;
        }
        if (n = this.tokenizer.tag(e)) {
          e = e.substring(n.raw.length), i = t[t.length - 1], i && n.type === "text" && i.type === "text" ? (i.raw += n.raw, i.text += n.text) : t.push(n);
          continue;
        }
        if (n = this.tokenizer.link(e)) {
          e = e.substring(n.raw.length), t.push(n);
          continue;
        }
        if (n = this.tokenizer.reflink(e, this.tokens.links)) {
          e = e.substring(n.raw.length), i = t[t.length - 1], i && n.type === "text" && i.type === "text" ? (i.raw += n.raw, i.text += n.text) : t.push(n);
          continue;
        }
        if (n = this.tokenizer.emStrong(e, s, u)) {
          e = e.substring(n.raw.length), t.push(n);
          continue;
        }
        if (n = this.tokenizer.codespan(e)) {
          e = e.substring(n.raw.length), t.push(n);
          continue;
        }
        if (n = this.tokenizer.br(e)) {
          e = e.substring(n.raw.length), t.push(n);
          continue;
        }
        if (n = this.tokenizer.del(e)) {
          e = e.substring(n.raw.length), t.push(n);
          continue;
        }
        if (n = this.tokenizer.autolink(e)) {
          e = e.substring(n.raw.length), t.push(n);
          continue;
        }
        if (!this.state.inLink && (n = this.tokenizer.url(e))) {
          e = e.substring(n.raw.length), t.push(n);
          continue;
        }
        if (l = e, this.options.extensions && this.options.extensions.startInline) {
          let c = 1 / 0;
          const h = e.slice(1);
          let p;
          this.options.extensions.startInline.forEach((g) => {
            p = g.call({ lexer: this }, h), typeof p == "number" && p >= 0 && (c = Math.min(c, p));
          }), c < 1 / 0 && c >= 0 && (l = e.substring(0, c + 1));
        }
        if (n = this.tokenizer.inlineText(l)) {
          e = e.substring(n.raw.length), n.raw.slice(-1) !== "_" && (u = n.raw.slice(-1)), a = !0, i = t[t.length - 1], i && i.type === "text" ? (i.raw += n.raw, i.text += n.text) : t.push(n);
          continue;
        }
        if (e) {
          const c = "Infinite loop on byte: " + e.charCodeAt(0);
          if (this.options.silent) {
            console.error(c);
            break;
          } else
            throw new Error(c);
        }
      }
    return t;
  }
}
class le {
  constructor(e) {
    x(this, "options");
    this.options = e || O;
  }
  code(e, t, n) {
    var l;
    const i = (l = (t || "").match(/^\S*/)) == null ? void 0 : l[0];
    return e = e.replace(/\n$/, "") + `
`, i ? '<pre><code class="language-' + C(i) + '">' + (n ? e : C(e, !0)) + `</code></pre>
` : "<pre><code>" + (n ? e : C(e, !0)) + `</code></pre>
`;
  }
  blockquote(e) {
    return `<blockquote>
${e}</blockquote>
`;
  }
  html(e, t) {
    return e;
  }
  heading(e, t, n) {
    return `<h${t}>${e}</h${t}>
`;
  }
  hr() {
    return `<hr>
`;
  }
  list(e, t, n) {
    const i = t ? "ol" : "ul", l = t && n !== 1 ? ' start="' + n + '"' : "";
    return "<" + i + l + `>
` + e + "</" + i + `>
`;
  }
  listitem(e, t, n) {
    return `<li>${e}</li>
`;
  }
  checkbox(e) {
    return "<input " + (e ? 'checked="" ' : "") + 'disabled="" type="checkbox">';
  }
  paragraph(e) {
    return `<p>${e}</p>
`;
  }
  table(e, t) {
    return t && (t = `<tbody>${t}</tbody>`), `<table>
<thead>
` + e + `</thead>
` + t + `</table>
`;
  }
  tablerow(e) {
    return `<tr>
${e}</tr>
`;
  }
  tablecell(e, t) {
    const n = t.header ? "th" : "td";
    return (t.align ? `<${n} align="${t.align}">` : `<${n}>`) + e + `</${n}>
`;
  }
  /**
   * span level renderer
   */
  strong(e) {
    return `<strong>${e}</strong>`;
  }
  em(e) {
    return `<em>${e}</em>`;
  }
  codespan(e) {
    return `<code>${e}</code>`;
  }
  br() {
    return "<br>";
  }
  del(e) {
    return `<del>${e}</del>`;
  }
  link(e, t, n) {
    const i = Ie(e);
    if (i === null)
      return n;
    e = i;
    let l = '<a href="' + e + '"';
    return t && (l += ' title="' + t + '"'), l += ">" + n + "</a>", l;
  }
  image(e, t, n) {
    const i = Ie(e);
    if (i === null)
      return n;
    e = i;
    let l = `<img src="${e}" alt="${n}"`;
    return t && (l += ` title="${t}"`), l += ">", l;
  }
  text(e) {
    return e;
  }
}
class we {
  // no need for block level renderers
  strong(e) {
    return e;
  }
  em(e) {
    return e;
  }
  codespan(e) {
    return e;
  }
  del(e) {
    return e;
  }
  html(e) {
    return e;
  }
  text(e) {
    return e;
  }
  link(e, t, n) {
    return "" + n;
  }
  image(e, t, n) {
    return "" + n;
  }
  br() {
    return "";
  }
}
class P {
  constructor(e) {
    x(this, "options");
    x(this, "renderer");
    x(this, "textRenderer");
    this.options = e || O, this.options.renderer = this.options.renderer || new le(), this.renderer = this.options.renderer, this.renderer.options = this.options, this.textRenderer = new we();
  }
  /**
   * Static Parse Method
   */
  static parse(e, t) {
    return new P(t).parse(e);
  }
  /**
   * Static Parse Inline Method
   */
  static parseInline(e, t) {
    return new P(t).parseInline(e);
  }
  /**
   * Parse Loop
   */
  parse(e, t = !0) {
    let n = "";
    for (let i = 0; i < e.length; i++) {
      const l = e[i];
      if (this.options.extensions && this.options.extensions.renderers && this.options.extensions.renderers[l.type]) {
        const s = l, o = this.options.extensions.renderers[s.type].call({ parser: this }, s);
        if (o !== !1 || !["space", "hr", "heading", "code", "table", "blockquote", "list", "html", "paragraph", "text"].includes(s.type)) {
          n += o || "";
          continue;
        }
      }
      switch (l.type) {
        case "space":
          continue;
        case "hr": {
          n += this.renderer.hr();
          continue;
        }
        case "heading": {
          const s = l;
          n += this.renderer.heading(this.parseInline(s.tokens), s.depth, ht(this.parseInline(s.tokens, this.textRenderer)));
          continue;
        }
        case "code": {
          const s = l;
          n += this.renderer.code(s.text, s.lang, !!s.escaped);
          continue;
        }
        case "table": {
          const s = l;
          let o = "", a = "";
          for (let c = 0; c < s.header.length; c++)
            a += this.renderer.tablecell(this.parseInline(s.header[c].tokens), { header: !0, align: s.align[c] });
          o += this.renderer.tablerow(a);
          let u = "";
          for (let c = 0; c < s.rows.length; c++) {
            const h = s.rows[c];
            a = "";
            for (let p = 0; p < h.length; p++)
              a += this.renderer.tablecell(this.parseInline(h[p].tokens), { header: !1, align: s.align[p] });
            u += this.renderer.tablerow(a);
          }
          n += this.renderer.table(o, u);
          continue;
        }
        case "blockquote": {
          const s = l, o = this.parse(s.tokens);
          n += this.renderer.blockquote(o);
          continue;
        }
        case "list": {
          const s = l, o = s.ordered, a = s.start, u = s.loose;
          let c = "";
          for (let h = 0; h < s.items.length; h++) {
            const p = s.items[h], g = p.checked, _ = p.task;
            let y = "";
            if (p.task) {
              const z = this.renderer.checkbox(!!g);
              u ? p.tokens.length > 0 && p.tokens[0].type === "paragraph" ? (p.tokens[0].text = z + " " + p.tokens[0].text, p.tokens[0].tokens && p.tokens[0].tokens.length > 0 && p.tokens[0].tokens[0].type === "text" && (p.tokens[0].tokens[0].text = z + " " + p.tokens[0].tokens[0].text)) : p.tokens.unshift({
                type: "text",
                text: z + " "
              }) : y += z + " ";
            }
            y += this.parse(p.tokens, u), c += this.renderer.listitem(y, _, !!g);
          }
          n += this.renderer.list(c, o, a);
          continue;
        }
        case "html": {
          const s = l;
          n += this.renderer.html(s.text, s.block);
          continue;
        }
        case "paragraph": {
          const s = l;
          n += this.renderer.paragraph(this.parseInline(s.tokens));
          continue;
        }
        case "text": {
          let s = l, o = s.tokens ? this.parseInline(s.tokens) : s.text;
          for (; i + 1 < e.length && e[i + 1].type === "text"; )
            s = e[++i], o += `
` + (s.tokens ? this.parseInline(s.tokens) : s.text);
          n += t ? this.renderer.paragraph(o) : o;
          continue;
        }
        default: {
          const s = 'Token with "' + l.type + '" type was not found.';
          if (this.options.silent)
            return console.error(s), "";
          throw new Error(s);
        }
      }
    }
    return n;
  }
  /**
   * Parse Inline Tokens
   */
  parseInline(e, t) {
    t = t || this.renderer;
    let n = "";
    for (let i = 0; i < e.length; i++) {
      const l = e[i];
      if (this.options.extensions && this.options.extensions.renderers && this.options.extensions.renderers[l.type]) {
        const s = this.options.extensions.renderers[l.type].call({ parser: this }, l);
        if (s !== !1 || !["escape", "html", "link", "image", "strong", "em", "codespan", "br", "del", "text"].includes(l.type)) {
          n += s || "";
          continue;
        }
      }
      switch (l.type) {
        case "escape": {
          const s = l;
          n += t.text(s.text);
          break;
        }
        case "html": {
          const s = l;
          n += t.html(s.text);
          break;
        }
        case "link": {
          const s = l;
          n += t.link(s.href, s.title, this.parseInline(s.tokens, t));
          break;
        }
        case "image": {
          const s = l;
          n += t.image(s.href, s.title, s.text);
          break;
        }
        case "strong": {
          const s = l;
          n += t.strong(this.parseInline(s.tokens, t));
          break;
        }
        case "em": {
          const s = l;
          n += t.em(this.parseInline(s.tokens, t));
          break;
        }
        case "codespan": {
          const s = l;
          n += t.codespan(s.text);
          break;
        }
        case "br": {
          n += t.br();
          break;
        }
        case "del": {
          const s = l;
          n += t.del(this.parseInline(s.tokens, t));
          break;
        }
        case "text": {
          const s = l;
          n += t.text(s.text);
          break;
        }
        default: {
          const s = 'Token with "' + l.type + '" type was not found.';
          if (this.options.silent)
            return console.error(s), "";
          throw new Error(s);
        }
      }
    }
    return n;
  }
}
class G {
  constructor(e) {
    x(this, "options");
    this.options = e || O;
  }
  /**
   * Process markdown before marked
   */
  preprocess(e) {
    return e;
  }
  /**
   * Process HTML after marked is finished
   */
  postprocess(e) {
    return e;
  }
  /**
   * Process all tokens before walk tokens
   */
  processAllTokens(e) {
    return e;
  }
}
x(G, "passThroughHooks", /* @__PURE__ */ new Set([
  "preprocess",
  "postprocess",
  "processAllTokens"
]));
var Z, pe, Ge;
class Ot {
  constructor(...e) {
    Te(this, Z);
    x(this, "defaults", fe());
    x(this, "options", this.setOptions);
    x(this, "parse", ee(this, Z, pe).call(this, M.lex, P.parse));
    x(this, "parseInline", ee(this, Z, pe).call(this, M.lexInline, P.parseInline));
    x(this, "Parser", P);
    x(this, "Renderer", le);
    x(this, "TextRenderer", we);
    x(this, "Lexer", M);
    x(this, "Tokenizer", se);
    x(this, "Hooks", G);
    this.use(...e);
  }
  /**
   * Run callback for every token
   */
  walkTokens(e, t) {
    var i, l;
    let n = [];
    for (const s of e)
      switch (n = n.concat(t.call(this, s)), s.type) {
        case "table": {
          const o = s;
          for (const a of o.header)
            n = n.concat(this.walkTokens(a.tokens, t));
          for (const a of o.rows)
            for (const u of a)
              n = n.concat(this.walkTokens(u.tokens, t));
          break;
        }
        case "list": {
          const o = s;
          n = n.concat(this.walkTokens(o.items, t));
          break;
        }
        default: {
          const o = s;
          (l = (i = this.defaults.extensions) == null ? void 0 : i.childTokens) != null && l[o.type] ? this.defaults.extensions.childTokens[o.type].forEach((a) => {
            const u = o[a].flat(1 / 0);
            n = n.concat(this.walkTokens(u, t));
          }) : o.tokens && (n = n.concat(this.walkTokens(o.tokens, t)));
        }
      }
    return n;
  }
  use(...e) {
    const t = this.defaults.extensions || { renderers: {}, childTokens: {} };
    return e.forEach((n) => {
      const i = { ...n };
      if (i.async = this.defaults.async || i.async || !1, n.extensions && (n.extensions.forEach((l) => {
        if (!l.name)
          throw new Error("extension name required");
        if ("renderer" in l) {
          const s = t.renderers[l.name];
          s ? t.renderers[l.name] = function(...o) {
            let a = l.renderer.apply(this, o);
            return a === !1 && (a = s.apply(this, o)), a;
          } : t.renderers[l.name] = l.renderer;
        }
        if ("tokenizer" in l) {
          if (!l.level || l.level !== "block" && l.level !== "inline")
            throw new Error("extension level must be 'block' or 'inline'");
          const s = t[l.level];
          s ? s.unshift(l.tokenizer) : t[l.level] = [l.tokenizer], l.start && (l.level === "block" ? t.startBlock ? t.startBlock.push(l.start) : t.startBlock = [l.start] : l.level === "inline" && (t.startInline ? t.startInline.push(l.start) : t.startInline = [l.start]));
        }
        "childTokens" in l && l.childTokens && (t.childTokens[l.name] = l.childTokens);
      }), i.extensions = t), n.renderer) {
        const l = this.defaults.renderer || new le(this.defaults);
        for (const s in n.renderer) {
          if (!(s in l))
            throw new Error(`renderer '${s}' does not exist`);
          if (s === "options")
            continue;
          const o = s, a = n.renderer[o], u = l[o];
          l[o] = (...c) => {
            let h = a.apply(l, c);
            return h === !1 && (h = u.apply(l, c)), h || "";
          };
        }
        i.renderer = l;
      }
      if (n.tokenizer) {
        const l = this.defaults.tokenizer || new se(this.defaults);
        for (const s in n.tokenizer) {
          if (!(s in l))
            throw new Error(`tokenizer '${s}' does not exist`);
          if (["options", "rules", "lexer"].includes(s))
            continue;
          const o = s, a = n.tokenizer[o], u = l[o];
          l[o] = (...c) => {
            let h = a.apply(l, c);
            return h === !1 && (h = u.apply(l, c)), h;
          };
        }
        i.tokenizer = l;
      }
      if (n.hooks) {
        const l = this.defaults.hooks || new G();
        for (const s in n.hooks) {
          if (!(s in l))
            throw new Error(`hook '${s}' does not exist`);
          if (s === "options")
            continue;
          const o = s, a = n.hooks[o], u = l[o];
          G.passThroughHooks.has(s) ? l[o] = (c) => {
            if (this.defaults.async)
              return Promise.resolve(a.call(l, c)).then((p) => u.call(l, p));
            const h = a.call(l, c);
            return u.call(l, h);
          } : l[o] = (...c) => {
            let h = a.apply(l, c);
            return h === !1 && (h = u.apply(l, c)), h;
          };
        }
        i.hooks = l;
      }
      if (n.walkTokens) {
        const l = this.defaults.walkTokens, s = n.walkTokens;
        i.walkTokens = function(o) {
          let a = [];
          return a.push(s.call(this, o)), l && (a = a.concat(l.call(this, o))), a;
        };
      }
      this.defaults = { ...this.defaults, ...i };
    }), this;
  }
  setOptions(e) {
    return this.defaults = { ...this.defaults, ...e }, this;
  }
  lexer(e, t) {
    return M.lex(e, t ?? this.defaults);
  }
  parser(e, t) {
    return P.parse(e, t ?? this.defaults);
  }
}
Z = new WeakSet(), pe = function(e, t) {
  return (n, i) => {
    const l = { ...i }, s = { ...this.defaults, ...l };
    this.defaults.async === !0 && l.async === !1 && (s.silent || console.warn("marked(): The async option was set to true by an extension. The async: false option sent to parse will be ignored."), s.async = !0);
    const o = ee(this, Z, Ge).call(this, !!s.silent, !!s.async);
    if (typeof n > "u" || n === null)
      return o(new Error("marked(): input parameter is undefined or null"));
    if (typeof n != "string")
      return o(new Error("marked(): input parameter is of type " + Object.prototype.toString.call(n) + ", string expected"));
    if (s.hooks && (s.hooks.options = s), s.async)
      return Promise.resolve(s.hooks ? s.hooks.preprocess(n) : n).then((a) => e(a, s)).then((a) => s.hooks ? s.hooks.processAllTokens(a) : a).then((a) => s.walkTokens ? Promise.all(this.walkTokens(a, s.walkTokens)).then(() => a) : a).then((a) => t(a, s)).then((a) => s.hooks ? s.hooks.postprocess(a) : a).catch(o);
    try {
      s.hooks && (n = s.hooks.preprocess(n));
      let a = e(n, s);
      s.hooks && (a = s.hooks.processAllTokens(a)), s.walkTokens && this.walkTokens(a, s.walkTokens);
      let u = t(a, s);
      return s.hooks && (u = s.hooks.postprocess(u)), u;
    } catch (a) {
      return o(a);
    }
  };
}, Ge = function(e, t) {
  return (n) => {
    if (n.message += `
Please report this to https://github.com/markedjs/marked.`, e) {
      const i = "<p>An error occurred:</p><pre>" + C(n.message + "", !0) + "</pre>";
      return t ? Promise.resolve(i) : i;
    }
    if (t)
      return Promise.reject(n);
    throw n;
  };
};
const D = new Ot();
function b(r, e) {
  return D.parse(r, e);
}
b.options = b.setOptions = function(r) {
  return D.setOptions(r), b.defaults = D.defaults, qe(b.defaults), b;
};
b.getDefaults = fe;
b.defaults = O;
b.use = function(...r) {
  return D.use(...r), b.defaults = D.defaults, qe(b.defaults), b;
};
b.walkTokens = function(r, e) {
  return D.walkTokens(r, e);
};
b.parseInline = D.parseInline;
b.Parser = P;
b.parser = P.parse;
b.Renderer = le;
b.TextRenderer = we;
b.Lexer = M;
b.lexer = M.lex;
b.Tokenizer = se;
b.Hooks = G;
b.parse = b;
b.options;
b.setOptions;
b.use;
b.walkTokens;
b.parseInline;
P.parse;
M.lex;
const {
  HtmlTagHydration: jt,
  SvelteComponent: Qt,
  append_hydration: I,
  attr: k,
  children: L,
  claim_element: S,
  claim_html_tag: Vt,
  claim_space: V,
  claim_text: ae,
  destroy_each: Nt,
  detach: v,
  element: A,
  ensure_array_like: Ee,
  init: Ht,
  insert_hydration: q,
  listen: Ue,
  noop: Le,
  null_to_empty: Ce,
  safe_not_equal: Ft,
  set_data: ce,
  set_style: j,
  space: N,
  src_url_equal: re,
  text: he,
  toggle_class: B
} = window.__gradio__svelte__internal;
function $e(r, e, t) {
  const n = r.slice();
  return n[31] = e[t], n[33] = t, n;
}
function Be(r) {
  let e, t, n, i = (
    /*label_icon*/
    r[0] && Me(r)
  );
  return {
    c() {
      e = A("label"), i && i.c(), t = N(), n = he(
        /*label*/
        r[3]
      ), this.h();
    },
    l(l) {
      e = S(l, "LABEL", { class: !0, for: !0 });
      var s = L(e);
      i && i.l(s), t = V(s), n = ae(
        s,
        /*label*/
        r[3]
      ), s.forEach(v), this.h();
    },
    h() {
      k(e, "class", "block-title svelte-h3uhc0"), k(e, "for", "consilium-roundtable");
    },
    m(l, s) {
      q(l, e, s), i && i.m(e, null), I(e, t), I(e, n);
    },
    p(l, s) {
      /*label_icon*/
      l[0] ? i ? i.p(l, s) : (i = Me(l), i.c(), i.m(e, t)) : i && (i.d(1), i = null), s[0] & /*label*/
      8 && ce(
        n,
        /*label*/
        l[3]
      );
    },
    d(l) {
      l && v(e), i && i.d();
    }
  };
}
function Me(r) {
  let e, t;
  function n(s, o) {
    return o[0] & /*label_icon*/
    1 && (t = null), t == null && (t = !!Yt(
      /*label_icon*/
      s[0]
    )), t ? Ut : Gt;
  }
  let i = n(r, [-1, -1]), l = i(r);
  return {
    c() {
      e = A("div"), l.c(), this.h();
    },
    l(s) {
      e = S(s, "DIV", { class: !0 });
      var o = L(e);
      l.l(o), o.forEach(v), this.h();
    },
    h() {
      k(e, "class", "label-icon-container svelte-h3uhc0");
    },
    m(s, o) {
      q(s, e, o), l.m(e, null);
    },
    p(s, o) {
      i === (i = n(s, o)) && l ? l.p(s, o) : (l.d(1), l = i(s), l && (l.c(), l.m(e, null)));
    },
    d(s) {
      s && v(e), l.d();
    }
  };
}
function Gt(r) {
  let e, t;
  return {
    c() {
      e = A("span"), t = he(
        /*label_icon*/
        r[0]
      ), this.h();
    },
    l(n) {
      e = S(n, "SPAN", { class: !0 });
      var i = L(e);
      t = ae(
        i,
        /*label_icon*/
        r[0]
      ), i.forEach(v), this.h();
    },
    h() {
      k(e, "class", "label-icon-emoji svelte-h3uhc0");
    },
    m(n, i) {
      q(n, e, i), I(e, t);
    },
    p(n, i) {
      i[0] & /*label_icon*/
      1 && ce(
        t,
        /*label_icon*/
        n[0]
      );
    },
    d(n) {
      n && v(e);
    }
  };
}
function Ut(r) {
  let e, t, n, i;
  return {
    c() {
      e = A("img"), this.h();
    },
    l(l) {
      e = S(l, "IMG", { src: !0, alt: !0, class: !0 }), this.h();
    },
    h() {
      re(e.src, t = /*label_icon*/
      r[0]) || k(e, "src", t), k(e, "alt", "Label Icon"), k(e, "class", "label-icon-image svelte-h3uhc0");
    },
    m(l, s) {
      q(l, e, s), n || (i = Ue(
        e,
        "error",
        /*handleLabelIconError*/
        r[19]
      ), n = !0);
    },
    p(l, s) {
      s[0] & /*label_icon*/
      1 && !re(e.src, t = /*label_icon*/
      l[0]) && k(e, "src", t);
    },
    d(l) {
      l && v(e), n = !1, i();
    }
  };
}
function Wt(r) {
  let e, t = (
    /*getEmoji*/
    r[12](
      /*participant*/
      r[31]
    ) + ""
  ), n;
  return {
    c() {
      e = A("span"), n = he(t), this.h();
    },
    l(i) {
      e = S(i, "SPAN", { class: !0 });
      var l = L(e);
      n = ae(l, t), l.forEach(v), this.h();
    },
    h() {
      k(e, "class", "avatar-emoji svelte-h3uhc0");
    },
    m(i, l) {
      q(i, e, l), I(e, n);
    },
    p(i, l) {
      l[0] & /*participants*/
      32 && t !== (t = /*getEmoji*/
      i[12](
        /*participant*/
        i[31]
      ) + "") && ce(n, t);
    },
    d(i) {
      i && v(e);
    }
  };
}
function Xt(r) {
  let e, t, n, i, l;
  function s(...o) {
    return (
      /*error_handler*/
      r[25](
        /*participant*/
        r[31],
        ...o
      )
    );
  }
  return {
    c() {
      e = A("img"), this.h();
    },
    l(o) {
      e = S(o, "IMG", { src: !0, alt: !0, class: !0 }), this.h();
    },
    h() {
      re(e.src, t = /*getAvatarImageUrl*/
      r[13](
        /*participant*/
        r[31]
      )) || k(e, "src", t), k(e, "alt", n = /*participant*/
      r[31]), k(e, "class", "avatar-image svelte-h3uhc0");
    },
    m(o, a) {
      q(o, e, a), i || (l = Ue(e, "error", s), i = !0);
    },
    p(o, a) {
      r = o, a[0] & /*participants*/
      32 && !re(e.src, t = /*getAvatarImageUrl*/
      r[13](
        /*participant*/
        r[31]
      )) && k(e, "src", t), a[0] & /*participants*/
      32 && n !== (n = /*participant*/
      r[31]) && k(e, "alt", n);
    },
    d(o) {
      o && v(e), i = !1, l();
    }
  };
}
function Pe(r) {
  let e, t, n, i, l = (
    /*renderMarkdown*/
    r[11](
      /*getLatestMessage*/
      r[15](
        /*participant*/
        r[31]
      )
    ) + ""
  ), s, o, a, u, c, h, p, g = (
    /*participant*/
    r[31] + ""
  ), _, y;
  function z(d, m) {
    return m[0] & /*participants*/
    32 && (c = null), c == null && (c = !!/*hasCustomImage*/
    d[14](
      /*participant*/
      d[31]
    )), c ? Xt : Wt;
  }
  let $ = z(r, [-1, -1]), T = $(r);
  return {
    c() {
      e = A("div"), t = A("div"), n = A("div"), i = new jt(!1), s = N(), o = A("div"), a = N(), u = A("div"), T.c(), h = N(), p = A("div"), _ = he(g), y = N(), this.h();
    },
    l(d) {
      e = S(d, "DIV", { class: !0, style: !0 });
      var m = L(e);
      t = S(m, "DIV", { class: !0 });
      var R = L(t);
      n = S(R, "DIV", { class: !0 });
      var X = L(n);
      i = Vt(X, !1), X.forEach(v), s = V(R), o = S(R, "DIV", { class: !0 }), L(o).forEach(v), R.forEach(v), a = V(m), u = S(m, "DIV", { class: !0, role: !0, tabindex: !0 });
      var J = L(u);
      T.l(J), J.forEach(v), h = V(m), p = S(m, "DIV", { class: !0 });
      var Y = L(p);
      _ = ae(Y, g), Y.forEach(v), y = V(m), m.forEach(v), this.h();
    },
    h() {
      i.a = null, k(n, "class", "bubble-content svelte-h3uhc0"), k(o, "class", "bubble-arrow svelte-h3uhc0"), k(t, "class", "speech-bubble svelte-h3uhc0"), B(
        t,
        "visible",
        /*isBubbleVisible*/
        r[16](
          /*participant*/
          r[31]
        )
      ), k(u, "class", "avatar svelte-h3uhc0"), k(u, "role", "button"), k(u, "tabindex", "0"), B(
        u,
        "speaking",
        /*isAvatarActive*/
        r[17](
          /*participant*/
          r[31]
        )
      ), B(
        u,
        "thinking",
        /*thinking*/
        r[7].includes(
          /*participant*/
          r[31]
        )
      ), B(
        u,
        "responding",
        /*currentSpeaker*/
        r[6] === /*participant*/
        r[31]
      ), B(
        u,
        "has-image",
        /*hasCustomImage*/
        r[14](
          /*participant*/
          r[31]
        )
      ), k(p, "class", "participant-name svelte-h3uhc0"), k(e, "class", "participant-seat svelte-h3uhc0"), j(e, "left", Q(
        /*index*/
        r[33],
        /*participants*/
        r[5].length
      ).left), j(e, "top", Q(
        /*index*/
        r[33],
        /*participants*/
        r[5].length
      ).top), j(e, "transform", Q(
        /*index*/
        r[33],
        /*participants*/
        r[5].length
      ).transform);
    },
    m(d, m) {
      q(d, e, m), I(e, t), I(t, n), i.m(l, n), I(t, s), I(t, o), I(e, a), I(e, u), T.m(u, null), I(e, h), I(e, p), I(p, _), I(e, y);
    },
    p(d, m) {
      m[0] & /*participants*/
      32 && l !== (l = /*renderMarkdown*/
      d[11](
        /*getLatestMessage*/
        d[15](
          /*participant*/
          d[31]
        )
      ) + "") && i.p(l), m[0] & /*isBubbleVisible, participants*/
      65568 && B(
        t,
        "visible",
        /*isBubbleVisible*/
        d[16](
          /*participant*/
          d[31]
        )
      ), $ === ($ = z(d, m)) && T ? T.p(d, m) : (T.d(1), T = $(d), T && (T.c(), T.m(u, null))), m[0] & /*isAvatarActive, participants*/
      131104 && B(
        u,
        "speaking",
        /*isAvatarActive*/
        d[17](
          /*participant*/
          d[31]
        )
      ), m[0] & /*thinking, participants*/
      160 && B(
        u,
        "thinking",
        /*thinking*/
        d[7].includes(
          /*participant*/
          d[31]
        )
      ), m[0] & /*currentSpeaker, participants*/
      96 && B(
        u,
        "responding",
        /*currentSpeaker*/
        d[6] === /*participant*/
        d[31]
      ), m[0] & /*hasCustomImage, participants*/
      16416 && B(
        u,
        "has-image",
        /*hasCustomImage*/
        d[14](
          /*participant*/
          d[31]
        )
      ), m[0] & /*participants*/
      32 && g !== (g = /*participant*/
      d[31] + "") && ce(_, g), m[0] & /*participants*/
      32 && j(e, "left", Q(
        /*index*/
        d[33],
        /*participants*/
        d[5].length
      ).left), m[0] & /*participants*/
      32 && j(e, "top", Q(
        /*index*/
        d[33],
        /*participants*/
        d[5].length
      ).top), m[0] & /*participants*/
      32 && j(e, "transform", Q(
        /*index*/
        d[33],
        /*participants*/
        d[5].length
      ).transform);
    },
    d(d) {
      d && v(e), T.d();
    }
  };
}
function Jt(r) {
  let e, t, n, i, l, s, o, a = (
    /*show_label*/
    r[4] && /*label*/
    r[3] && Be(r)
  ), u = Ee(
    /*participants*/
    r[5]
  ), c = [];
  for (let h = 0; h < u.length; h += 1)
    c[h] = Pe($e(r, u, h));
  return {
    c() {
      e = A("div"), t = A("div"), n = A("div"), a && a.c(), i = N(), l = A("div");
      for (let h = 0; h < c.length; h += 1)
        c[h].c();
      this.h();
    },
    l(h) {
      e = S(h, "DIV", { class: !0, id: !0, style: !0 });
      var p = L(e);
      t = S(p, "DIV", { class: !0, id: !0 });
      var g = L(t);
      n = S(g, "DIV", { class: !0 });
      var _ = L(n);
      a && a.l(_), _.forEach(v), i = V(g), l = S(g, "DIV", { class: !0 });
      var y = L(l);
      for (let z = 0; z < c.length; z += 1)
        c[z].l(y);
      y.forEach(v), g.forEach(v), p.forEach(v), this.h();
    },
    h() {
      k(n, "class", "table-center svelte-h3uhc0"), k(l, "class", "participants-circle"), k(t, "class", "consilium-container svelte-h3uhc0"), k(t, "id", "consilium-roundtable"), k(e, "class", s = Ce(
        /*containerClasses*/
        r[10]
      ) + " svelte-h3uhc0"), k(
        e,
        "id",
        /*elem_id*/
        r[1]
      ), k(e, "style", o = /*containerStyle*/
      r[9] + "; " + /*minWidthStyle*/
      r[8]), B(e, "hidden", !/*visible*/
      r[2]);
    },
    m(h, p) {
      q(h, e, p), I(e, t), I(t, n), a && a.m(n, null), I(t, i), I(t, l);
      for (let g = 0; g < c.length; g += 1)
        c[g] && c[g].m(l, null);
    },
    p(h, p) {
      if (/*show_label*/
      h[4] && /*label*/
      h[3] ? a ? a.p(h, p) : (a = Be(h), a.c(), a.m(n, null)) : a && (a.d(1), a = null), p[0] & /*participants, isAvatarActive, thinking, currentSpeaker, hasCustomImage, getAvatarImageUrl, handleImageError, getEmoji, isBubbleVisible, renderMarkdown, getLatestMessage*/
      522464) {
        u = Ee(
          /*participants*/
          h[5]
        );
        let g;
        for (g = 0; g < u.length; g += 1) {
          const _ = $e(h, u, g);
          c[g] ? c[g].p(_, p) : (c[g] = Pe(_), c[g].c(), c[g].m(l, null));
        }
        for (; g < c.length; g += 1)
          c[g].d(1);
        c.length = u.length;
      }
      p[0] & /*containerClasses*/
      1024 && s !== (s = Ce(
        /*containerClasses*/
        h[10]
      ) + " svelte-h3uhc0") && k(e, "class", s), p[0] & /*elem_id*/
      2 && k(
        e,
        "id",
        /*elem_id*/
        h[1]
      ), p[0] & /*containerStyle, minWidthStyle*/
      768 && o !== (o = /*containerStyle*/
      h[9] + "; " + /*minWidthStyle*/
      h[8]) && k(e, "style", o), p[0] & /*containerClasses, visible*/
      1028 && B(e, "hidden", !/*visible*/
      h[2]);
    },
    i: Le,
    o: Le,
    d(h) {
      h && v(e), a && a.d(), Nt(c, h);
    }
  };
}
function Q(r, e) {
  const n = (360 / e * r - 90) * (Math.PI / 180), i = 260, l = 180, s = Math.cos(n) * i, o = Math.sin(n) * l;
  return {
    left: `calc(50% + ${s}px)`,
    top: `calc(50% + ${o}px)`,
    transform: "translate(-50%, -50%)"
  };
}
function Yt(r) {
  return r ? r.startsWith("http://") || r.startsWith("https://") || r.startsWith("data:") : !1;
}
function Kt(r, e, t) {
  let n, i, l, { gradio: s } = e, { elem_id: o = "" } = e, { elem_classes: a = [] } = e, { visible: u = !0 } = e, { value: c = "{}" } = e, { label: h = "Consilium Roundtable" } = e, { label_icon: p = "🎭" } = e, { show_label: g = !0 } = e, { scale: _ = null } = e, { min_width: y = void 0 } = e, z = [], $ = [], T = null, d = [], m = [], R = {};
  function X() {
    try {
      const f = JSON.parse(c);
      t(5, z = f.participants || []), $ = f.messages || [], t(6, T = f.currentSpeaker || null), t(7, d = f.thinking || []), m = f.showBubbles || [], R = f.avatarImages || {}, console.log("Clean JSON parsed:", {
        participants: z,
        messages: $,
        currentSpeaker: T,
        thinking: d,
        showBubbles: m,
        avatarImages: R
      });
    } catch (f) {
      console.error("Invalid JSON:", c, f);
    }
  }
  function J(f) {
    if (!f) return f;
    try {
      return b.setOptions({
        breaks: !0,
        // Convert line breaks to <br>
        gfm: !0,
        // GitHub flavored markdown
        sanitize: !1,
        // Allow HTML (safe since we control input)
        smartypants: !1
        // Don't convert quotes/dashes
      }), f.includes(`
`) ? b.parse(f) : b.parseInline(f);
    } catch (E) {
      return console.error("Markdown parsing error:", E), f;
    }
  }
  const Y = {
    Anthropic: "🤖",
    Claude: "🤖",
    Search: "🔍",
    "Web Search Agent": "🔍",
    OpenAI: "🧠",
    "GPT-4": "🧠",
    Google: "💎",
    Gemini: "💎",
    "QwQ-32B": "😊",
    "DeepSeek-R1": "🔮",
    Mistral: "🐱",
    "Mistral Large": "🐱",
    "Meta-Llama-3.1-8B": "🦙"
  };
  function We(f) {
    return Y[f] || "🤖";
  }
  function Xe(f) {
    return R[f] || null;
  }
  function Je(f) {
    return R[f] && R[f].trim() !== "";
  }
  function Ye(f) {
    if (d.includes(f))
      return `${f} is thinking...`;
    if (T === f)
      return `${f} is responding...`;
    const E = $.filter((K) => K.speaker === f);
    return E.length === 0 ? `${f} is ready to discuss...` : E[E.length - 1].text || `${f} responded`;
  }
  function Ke(f) {
    const E = d.includes(f), K = T === f, _e = m.includes(f), ye = E || K || _e;
    return console.log(`${f} bubble visible:`, ye, { isThinking: E, isSpeaking: K, shouldShow: _e }), ye;
  }
  function et(f) {
    return d.includes(f) || T === f;
  }
  function xe(f, E) {
    console.warn(`Failed to load avatar image for ${E}, falling back to emoji`), R = Object.assign(Object.assign({}, R), { [E]: null });
  }
  function tt(f) {
    console.warn("Failed to load label icon image, falling back to default emoji"), t(0, p = null);
  }
  const nt = (f, E) => xe(E, f);
  return r.$$set = (f) => {
    "gradio" in f && t(20, s = f.gradio), "elem_id" in f && t(1, o = f.elem_id), "elem_classes" in f && t(21, a = f.elem_classes), "visible" in f && t(2, u = f.visible), "value" in f && t(22, c = f.value), "label" in f && t(3, h = f.label), "label_icon" in f && t(0, p = f.label_icon), "show_label" in f && t(4, g = f.show_label), "scale" in f && t(23, _ = f.scale), "min_width" in f && t(24, y = f.min_width);
  }, r.$$.update = () => {
    r.$$.dirty[0] & /*elem_classes*/
    2097152 && t(10, n = `wrapper ${a.join(" ")}`), r.$$.dirty[0] & /*scale*/
    8388608 && t(9, i = _ ? `--scale: ${_}` : ""), r.$$.dirty[0] & /*min_width*/
    16777216 && t(8, l = y ? `min-width: ${y}px` : ""), r.$$.dirty[0] & /*value*/
    4194304 && X();
  }, [
    p,
    o,
    u,
    h,
    g,
    z,
    T,
    d,
    l,
    i,
    n,
    J,
    We,
    Xe,
    Je,
    Ye,
    Ke,
    et,
    xe,
    tt,
    s,
    a,
    c,
    _,
    y,
    nt
  ];
}
class tn extends Qt {
  constructor(e) {
    super(), Ht(
      this,
      e,
      Kt,
      Jt,
      Ft,
      {
        gradio: 20,
        elem_id: 1,
        elem_classes: 21,
        visible: 2,
        value: 22,
        label: 3,
        label_icon: 0,
        show_label: 4,
        scale: 23,
        min_width: 24
      },
      null,
      [-1, -1]
    );
  }
}
export {
  tn as default
};
