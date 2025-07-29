var bt = Object.defineProperty;
var xt = (n, e, t) => e in n ? bt(n, e, { enumerable: !0, configurable: !0, writable: !0, value: t }) : n[e] = t;
var v = (n, e, t) => xt(n, typeof e != "symbol" ? e + "" : e, t);
function V() {
}
V.prototype = {
  diff: function(e, t) {
    var s, i = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : {}, r = i.callback;
    typeof i == "function" && (r = i, i = {}), this.options = i;
    var c = this;
    function l(R) {
      return r ? (setTimeout(function() {
        r(void 0, R);
      }, 0), !0) : R;
    }
    e = this.castInput(e), t = this.castInput(t), e = this.removeEmpty(this.tokenize(e)), t = this.removeEmpty(this.tokenize(t));
    var u = t.length, a = e.length, o = 1, p = u + a;
    i.maxEditLength && (p = Math.min(p, i.maxEditLength));
    var h = (s = i.timeout) !== null && s !== void 0 ? s : 1 / 0, d = Date.now() + h, f = [{
      oldPos: -1,
      lastComponent: void 0
    }], k = this.extractCommon(f[0], t, e, 0);
    if (f[0].oldPos + 1 >= a && k + 1 >= u)
      return l([{
        value: this.join(t),
        count: t.length
      }]);
    var g = -1 / 0, I = 1 / 0;
    function E() {
      for (var R = Math.max(g, -o); R <= Math.min(I, o); R += 2) {
        var q = void 0, $ = f[R - 1], z = f[R + 1];
        $ && (f[R - 1] = void 0);
        var j = !1;
        if (z) {
          var W = z.oldPos - R;
          j = z && 0 <= W && W < u;
        }
        var H = $ && $.oldPos + 1 < a;
        if (!j && !H) {
          f[R] = void 0;
          continue;
        }
        if (!H || j && $.oldPos + 1 < z.oldPos ? q = c.addToPath(z, !0, void 0, 0) : q = c.addToPath($, void 0, !0, 1), k = c.extractCommon(q, t, e, R), q.oldPos + 1 >= a && k + 1 >= u)
          return l(wt(c, q.lastComponent, t, e, c.useLongestToken));
        f[R] = q, q.oldPos + 1 >= a && (I = Math.min(I, R - 1)), k + 1 >= u && (g = Math.max(g, R + 1));
      }
      o++;
    }
    if (r)
      (function R() {
        setTimeout(function() {
          if (o > p || Date.now() > d)
            return r();
          E() || R();
        }, 0);
      })();
    else
      for (; o <= p && Date.now() <= d; ) {
        var B = E();
        if (B)
          return B;
      }
  },
  addToPath: function(e, t, s, i) {
    var r = e.lastComponent;
    return r && r.added === t && r.removed === s ? {
      oldPos: e.oldPos + i,
      lastComponent: {
        count: r.count + 1,
        added: t,
        removed: s,
        previousComponent: r.previousComponent
      }
    } : {
      oldPos: e.oldPos + i,
      lastComponent: {
        count: 1,
        added: t,
        removed: s,
        previousComponent: r
      }
    };
  },
  extractCommon: function(e, t, s, i) {
    for (var r = t.length, c = s.length, l = e.oldPos, u = l - i, a = 0; u + 1 < r && l + 1 < c && this.equals(t[u + 1], s[l + 1]); )
      u++, l++, a++;
    return a && (e.lastComponent = {
      count: a,
      previousComponent: e.lastComponent
    }), e.oldPos = l, u;
  },
  equals: function(e, t) {
    return this.options.comparator ? this.options.comparator(e, t) : e === t || this.options.ignoreCase && e.toLowerCase() === t.toLowerCase();
  },
  removeEmpty: function(e) {
    for (var t = [], s = 0; s < e.length; s++)
      e[s] && t.push(e[s]);
    return t;
  },
  castInput: function(e) {
    return e;
  },
  tokenize: function(e) {
    return e.split("");
  },
  join: function(e) {
    return e.join("");
  }
};
function wt(n, e, t, s, i) {
  for (var r = [], c; e; )
    r.push(e), c = e.previousComponent, delete e.previousComponent, e = c;
  r.reverse();
  for (var l = 0, u = r.length, a = 0, o = 0; l < u; l++) {
    var p = r[l];
    if (p.removed) {
      if (p.value = n.join(s.slice(o, o + p.count)), o += p.count, l && r[l - 1].added) {
        var d = r[l - 1];
        r[l - 1] = r[l], r[l] = d;
      }
    } else {
      if (!p.added && i) {
        var h = t.slice(a, a + p.count);
        h = h.map(function(k, g) {
          var I = s[o + g];
          return I.length > k.length ? I : k;
        }), p.value = n.join(h);
      } else
        p.value = n.join(t.slice(a, a + p.count));
      a += p.count, p.added || (o += p.count);
    }
  }
  var f = r[u - 1];
  return u > 1 && typeof f.value == "string" && (f.added || f.removed) && n.equals("", f.value) && (r[u - 2].value += f.value, r.pop()), r;
}
var vt = new V();
function _t(n, e, t) {
  return vt.diff(n, e, t);
}
var Ve = /^[A-Za-z\xC0-\u02C6\u02C8-\u02D7\u02DE-\u02FF\u1E00-\u1EFF]+$/, je = /\S/, rt = new V();
rt.equals = function(n, e) {
  return this.options.ignoreCase && (n = n.toLowerCase(), e = e.toLowerCase()), n === e || this.options.ignoreWhitespace && !je.test(n) && !je.test(e);
};
rt.tokenize = function(n) {
  for (var e = n.split(/([^\S\r\n]+|[()[\]{}'"\r\n]|\b)/), t = 0; t < e.length - 1; t++)
    !e[t + 1] && e[t + 2] && Ve.test(e[t]) && Ve.test(e[t + 2]) && (e[t] += e[t + 2], e.splice(t + 1, 2), t--);
  return e;
};
var lt = new V();
lt.tokenize = function(n) {
  this.options.stripTrailingCr && (n = n.replace(/\r\n/g, `
`));
  var e = [], t = n.split(/(\n|\r\n)/);
  t[t.length - 1] || t.pop();
  for (var s = 0; s < t.length; s++) {
    var i = t[s];
    s % 2 && !this.options.newlineIsToken ? e[e.length - 1] += i : (this.options.ignoreWhitespace && (i = i.trim()), e.push(i));
  }
  return e;
};
var yt = new V();
yt.tokenize = function(n) {
  return n.split(/(\S.+?[.!?])(?=\s+|$)/);
};
var Rt = new V();
Rt.tokenize = function(n) {
  return n.split(/([{}:;,]|\s+)/);
};
function ke(n) {
  "@babel/helpers - typeof";
  return typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? ke = function(e) {
    return typeof e;
  } : ke = function(e) {
    return e && typeof Symbol == "function" && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e;
  }, ke(n);
}
var Ct = Object.prototype.toString, oe = new V();
oe.useLongestToken = !0;
oe.tokenize = lt.tokenize;
oe.castInput = function(n) {
  var e = this.options, t = e.undefinedReplacement, s = e.stringifyReplacer, i = s === void 0 ? function(r, c) {
    return typeof c > "u" ? t : c;
  } : s;
  return typeof n == "string" ? n : JSON.stringify(Ce(n, null, null, i), i, "  ");
};
oe.equals = function(n, e) {
  return V.prototype.equals.call(oe, n.replace(/,([\r\n])/g, "$1"), e.replace(/,([\r\n])/g, "$1"));
};
function Ce(n, e, t, s, i) {
  e = e || [], t = t || [], s && (n = s(i, n));
  var r;
  for (r = 0; r < e.length; r += 1)
    if (e[r] === n)
      return t[r];
  var c;
  if (Ct.call(n) === "[object Array]") {
    for (e.push(n), c = new Array(n.length), t.push(c), r = 0; r < n.length; r += 1)
      c[r] = Ce(n[r], e, t, s, i);
    return e.pop(), t.pop(), c;
  }
  if (n && n.toJSON && (n = n.toJSON()), ke(n) === "object" && n !== null) {
    e.push(n), c = {}, t.push(c);
    var l = [], u;
    for (u in n)
      n.hasOwnProperty(u) && l.push(u);
    for (l.sort(), r = 0; r < l.length; r += 1)
      u = l[r], c[u] = Ce(n[u], e, t, s, u);
    e.pop(), t.pop();
  } else
    c = n;
  return c;
}
var Te = new V();
Te.tokenize = function(n) {
  return n.slice();
};
Te.join = Te.removeEmpty = function(n) {
  return n;
};
function Le() {
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
var X = Le();
function at(n) {
  X = n;
}
var ae = { exec: () => null };
function w(n, e = "") {
  let t = typeof n == "string" ? n : n.source;
  const s = {
    replace: (i, r) => {
      let c = typeof r == "string" ? r : r.source;
      return c = c.replace(P.caret, "$1"), t = t.replace(i, c), s;
    },
    getRegex: () => new RegExp(t, e)
  };
  return s;
}
var P = {
  codeRemoveIndent: /^(?: {1,4}| {0,3}\t)/gm,
  outputLinkReplace: /\\([\[\]])/g,
  indentCodeCompensation: /^(\s+)(?:```)/,
  beginningSpace: /^\s+/,
  endingHash: /#$/,
  startingSpaceChar: /^ /,
  endingSpaceChar: / $/,
  nonSpaceChar: /[^ ]/,
  newLineCharGlobal: /\n/g,
  tabCharGlobal: /\t/g,
  multipleSpaceGlobal: /\s+/g,
  blankLine: /^[ \t]*$/,
  doubleBlankLine: /\n[ \t]*\n[ \t]*$/,
  blockquoteStart: /^ {0,3}>/,
  blockquoteSetextReplace: /\n {0,3}((?:=+|-+) *)(?=\n|$)/g,
  blockquoteSetextReplace2: /^ {0,3}>[ \t]?/gm,
  listReplaceTabs: /^\t+/,
  listReplaceNesting: /^ {1,4}(?=( {4})*[^ ])/g,
  listIsTask: /^\[[ xX]\] /,
  listReplaceTask: /^\[[ xX]\] +/,
  anyLine: /\n.*\n/,
  hrefBrackets: /^<(.*)>$/,
  tableDelimiter: /[:|]/,
  tableAlignChars: /^\||\| *$/g,
  tableRowBlankLine: /\n[ \t]*$/,
  tableAlignRight: /^ *-+: *$/,
  tableAlignCenter: /^ *:-+: *$/,
  tableAlignLeft: /^ *:-+ *$/,
  startATag: /^<a /i,
  endATag: /^<\/a>/i,
  startPreScriptTag: /^<(pre|code|kbd|script)(\s|>)/i,
  endPreScriptTag: /^<\/(pre|code|kbd|script)(\s|>)/i,
  startAngleBracket: /^</,
  endAngleBracket: />$/,
  pedanticHrefTitle: /^([^'"]*[^\s])\s+(['"])(.*)\2/,
  unicodeAlphaNumeric: /[\p{L}\p{N}]/u,
  escapeTest: /[&<>"']/,
  escapeReplace: /[&<>"']/g,
  escapeTestNoEncode: /[<>"']|&(?!(#\d{1,7}|#[Xx][a-fA-F0-9]{1,6}|\w+);)/,
  escapeReplaceNoEncode: /[<>"']|&(?!(#\d{1,7}|#[Xx][a-fA-F0-9]{1,6}|\w+);)/g,
  unescapeTest: /&(#(?:\d+)|(?:#x[0-9A-Fa-f]+)|(?:\w+));?/ig,
  caret: /(^|[^\[])\^/g,
  percentDecode: /%25/g,
  findPipe: /\|/g,
  splitPipe: / \|/,
  slashPipe: /\\\|/g,
  carriageReturn: /\r\n|\r/g,
  spaceLine: /^ +$/gm,
  notSpaceStart: /^\S*/,
  endingNewline: /\n$/,
  listItemRegex: (n) => new RegExp(`^( {0,3}${n})((?:[	 ][^\\n]*)?(?:\\n|$))`),
  nextBulletRegex: (n) => new RegExp(`^ {0,${Math.min(3, n - 1)}}(?:[*+-]|\\d{1,9}[.)])((?:[ 	][^\\n]*)?(?:\\n|$))`),
  hrRegex: (n) => new RegExp(`^ {0,${Math.min(3, n - 1)}}((?:- *){3,}|(?:_ *){3,}|(?:\\* *){3,})(?:\\n+|$)`),
  fencesBeginRegex: (n) => new RegExp(`^ {0,${Math.min(3, n - 1)}}(?:\`\`\`|~~~)`),
  headingBeginRegex: (n) => new RegExp(`^ {0,${Math.min(3, n - 1)}}#`),
  htmlBeginRegex: (n) => new RegExp(`^ {0,${Math.min(3, n - 1)}}<(?:[a-z].*>|!--)`, "i")
}, Tt = /^(?:[ \t]*(?:\n|$))+/, St = /^((?: {4}| {0,3}\t)[^\n]+(?:\n(?:[ \t]*(?:\n|$))*)?)+/, zt = /^ {0,3}(`{3,}(?=[^`\n]*(?:\n|$))|~{3,})([^\n]*)(?:\n|$)(?:|([\s\S]*?)(?:\n|$))(?: {0,3}\1[~`]* *(?=\n|$)|$)/, ce = /^ {0,3}((?:-[\t ]*){3,}|(?:_[ \t]*){3,}|(?:\*[ \t]*){3,})(?:\n+|$)/, $t = /^ {0,3}(#{1,6})(?=\s|$)(.*)(?:\n+|$)/, Ie = /(?:[*+-]|\d{1,9}[.)])/, ot = /^(?!bull |blockCode|fences|blockquote|heading|html|table)((?:.|\n(?!\s*?\n|bull |blockCode|fences|blockquote|heading|html|table))+?)\n {0,3}(=+|-+) *(?:\n+|$)/, ct = w(ot).replace(/bull/g, Ie).replace(/blockCode/g, /(?: {4}| {0,3}\t)/).replace(/fences/g, / {0,3}(?:`{3,}|~{3,})/).replace(/blockquote/g, / {0,3}>/).replace(/heading/g, / {0,3}#{1,6}/).replace(/html/g, / {0,3}<[^\n>]+>\n/).replace(/\|table/g, "").getRegex(), At = w(ot).replace(/bull/g, Ie).replace(/blockCode/g, /(?: {4}| {0,3}\t)/).replace(/fences/g, / {0,3}(?:`{3,}|~{3,})/).replace(/blockquote/g, / {0,3}>/).replace(/heading/g, / {0,3}#{1,6}/).replace(/html/g, / {0,3}<[^\n>]+>\n/).replace(/table/g, / {0,3}\|?(?:[:\- ]*\|)+[\:\- ]*\n/).getRegex(), Ee = /^([^\n]+(?:\n(?!hr|heading|lheading|blockquote|fences|list|html|table| +\n)[^\n]+)*)/, Lt = /^[^\n]+/, Pe = /(?!\s*\])(?:\\.|[^\[\]\\])+/, It = w(/^ {0,3}\[(label)\]: *(?:\n[ \t]*)?([^<\s][^\s]*|<.*?>)(?:(?: +(?:\n[ \t]*)?| *\n[ \t]*)(title))? *(?:\n+|$)/).replace("label", Pe).replace("title", /(?:"(?:\\"?|[^"\\])*"|'[^'\n]*(?:\n[^'\n]+)*\n?'|\([^()]*\))/).getRegex(), Et = w(/^( {0,3}bull)([ \t][^\n]+?)?(?:\n|$)/).replace(/bull/g, Ie).getRegex(), ve = "address|article|aside|base|basefont|blockquote|body|caption|center|col|colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|footer|form|frame|frameset|h[1-6]|head|header|hr|html|iframe|legend|li|link|main|menu|menuitem|meta|nav|noframes|ol|optgroup|option|p|param|search|section|summary|table|tbody|td|tfoot|th|thead|title|tr|track|ul", De = /<!--(?:-?>|[\s\S]*?(?:-->|$))/, Pt = w(
  "^ {0,3}(?:<(script|pre|style|textarea)[\\s>][\\s\\S]*?(?:</\\1>[^\\n]*\\n+|$)|comment[^\\n]*(\\n+|$)|<\\?[\\s\\S]*?(?:\\?>\\n*|$)|<![A-Z][\\s\\S]*?(?:>\\n*|$)|<!\\[CDATA\\[[\\s\\S]*?(?:\\]\\]>\\n*|$)|</?(tag)(?: +|\\n|/?>)[\\s\\S]*?(?:(?:\\n[ 	]*)+\\n|$)|<(?!script|pre|style|textarea)([a-z][\\w-]*)(?:attribute)*? */?>(?=[ \\t]*(?:\\n|$))[\\s\\S]*?(?:(?:\\n[ 	]*)+\\n|$)|</(?!script|pre|style|textarea)[a-z][\\w-]*\\s*>(?=[ \\t]*(?:\\n|$))[\\s\\S]*?(?:(?:\\n[ 	]*)+\\n|$))",
  "i"
).replace("comment", De).replace("tag", ve).replace("attribute", / +[a-zA-Z:_][\w.:-]*(?: *= *"[^"\n]*"| *= *'[^'\n]*'| *= *[^\s"'=<>`]+)?/).getRegex(), ut = w(Ee).replace("hr", ce).replace("heading", " {0,3}#{1,6}(?:\\s|$)").replace("|lheading", "").replace("|table", "").replace("blockquote", " {0,3}>").replace("fences", " {0,3}(?:`{3,}(?=[^`\\n]*\\n)|~{3,})[^\\n]*\\n").replace("list", " {0,3}(?:[*+-]|1[.)]) ").replace("html", "</?(?:tag)(?: +|\\n|/?>)|<(?:script|pre|style|textarea|!--)").replace("tag", ve).getRegex(), Dt = w(/^( {0,3}> ?(paragraph|[^\n]*)(?:\n|$))+/).replace("paragraph", ut).getRegex(), Be = {
  blockquote: Dt,
  code: St,
  def: It,
  fences: zt,
  heading: $t,
  hr: ce,
  html: Pt,
  lheading: ct,
  list: Et,
  newline: Tt,
  paragraph: ut,
  table: ae,
  text: Lt
}, We = w(
  "^ *([^\\n ].*)\\n {0,3}((?:\\| *)?:?-+:? *(?:\\| *:?-+:? *)*(?:\\| *)?)(?:\\n((?:(?! *\\n|hr|heading|blockquote|code|fences|list|html).*(?:\\n|$))*)\\n*|$)"
).replace("hr", ce).replace("heading", " {0,3}#{1,6}(?:\\s|$)").replace("blockquote", " {0,3}>").replace("code", "(?: {4}| {0,3}	)[^\\n]").replace("fences", " {0,3}(?:`{3,}(?=[^`\\n]*\\n)|~{3,})[^\\n]*\\n").replace("list", " {0,3}(?:[*+-]|1[.)]) ").replace("html", "</?(?:tag)(?: +|\\n|/?>)|<(?:script|pre|style|textarea|!--)").replace("tag", ve).getRegex(), Bt = {
  ...Be,
  lheading: At,
  table: We,
  paragraph: w(Ee).replace("hr", ce).replace("heading", " {0,3}#{1,6}(?:\\s|$)").replace("|lheading", "").replace("table", We).replace("blockquote", " {0,3}>").replace("fences", " {0,3}(?:`{3,}(?=[^`\\n]*\\n)|~{3,})[^\\n]*\\n").replace("list", " {0,3}(?:[*+-]|1[.)]) ").replace("html", "</?(?:tag)(?: +|\\n|/?>)|<(?:script|pre|style|textarea|!--)").replace("tag", ve).getRegex()
}, qt = {
  ...Be,
  html: w(
    `^ *(?:comment *(?:\\n|\\s*$)|<(tag)[\\s\\S]+?</\\1> *(?:\\n{2,}|\\s*$)|<tag(?:"[^"]*"|'[^']*'|\\s[^'"/>\\s]*)*?/?> *(?:\\n{2,}|\\s*$))`
  ).replace("comment", De).replace(/tag/g, "(?!(?:a|em|strong|small|s|cite|q|dfn|abbr|data|time|code|var|samp|kbd|sub|sup|i|b|u|mark|ruby|rt|rp|bdi|bdo|span|br|wbr|ins|del|img)\\b)\\w+(?!:|[^\\w\\s@]*@)\\b").getRegex(),
  def: /^ *\[([^\]]+)\]: *<?([^\s>]+)>?(?: +(["(][^\n]+[")]))? *(?:\n+|$)/,
  heading: /^(#{1,6})(.*)(?:\n+|$)/,
  fences: ae,
  // fences not supported
  lheading: /^(.+?)\n {0,3}(=+|-+) *(?:\n+|$)/,
  paragraph: w(Ee).replace("hr", ce).replace("heading", ` *#{1,6} *[^
]`).replace("lheading", ct).replace("|table", "").replace("blockquote", " {0,3}>").replace("|fences", "").replace("|list", "").replace("|html", "").replace("|tag", "").getRegex()
}, Nt = /^\\([!"#$%&'()*+,\-./:;<=>?@\[\]\\^_`{|}~])/, Ot = /^(`+)([^`]|[^`][\s\S]*?[^`])\1(?!`)/, ht = /^( {2,}|\\)\n(?!\s*$)/, Zt = /^(`+|[^`])(?:(?= {2,}\n)|[\s\S]*?(?:(?=[\\<!\[`*_]|\b_|$)|[^ ](?= {2,}\n)))/, _e = /[\p{P}\p{S}]/u, qe = /[\s\p{P}\p{S}]/u, pt = /[^\s\p{P}\p{S}]/u, Mt = w(/^((?![*_])punctSpace)/, "u").replace(/punctSpace/g, qe).getRegex(), ft = /(?!~)[\p{P}\p{S}]/u, Ht = /(?!~)[\s\p{P}\p{S}]/u, Gt = /(?:[^\s\p{P}\p{S}]|~)/u, Ft = /\[[^[\]]*?\]\((?:\\.|[^\\\(\)]|\((?:\\.|[^\\\(\)])*\))*\)|`[^`]*?`|<[^<>]*?>/g, dt = /^(?:\*+(?:((?!\*)punct)|[^\s*]))|^_+(?:((?!_)punct)|([^\s_]))/, Qt = w(dt, "u").replace(/punct/g, _e).getRegex(), Vt = w(dt, "u").replace(/punct/g, ft).getRegex(), gt = "^[^_*]*?__[^_*]*?\\*[^_*]*?(?=__)|[^*]+(?=[^*])|(?!\\*)punct(\\*+)(?=[\\s]|$)|notPunctSpace(\\*+)(?!\\*)(?=punctSpace|$)|(?!\\*)punctSpace(\\*+)(?=notPunctSpace)|[\\s](\\*+)(?!\\*)(?=punct)|(?!\\*)punct(\\*+)(?!\\*)(?=punct)|notPunctSpace(\\*+)(?=notPunctSpace)", jt = w(gt, "gu").replace(/notPunctSpace/g, pt).replace(/punctSpace/g, qe).replace(/punct/g, _e).getRegex(), Wt = w(gt, "gu").replace(/notPunctSpace/g, Gt).replace(/punctSpace/g, Ht).replace(/punct/g, ft).getRegex(), Ut = w(
  "^[^_*]*?\\*\\*[^_*]*?_[^_*]*?(?=\\*\\*)|[^_]+(?=[^_])|(?!_)punct(_+)(?=[\\s]|$)|notPunctSpace(_+)(?!_)(?=punctSpace|$)|(?!_)punctSpace(_+)(?=notPunctSpace)|[\\s](_+)(?!_)(?=punct)|(?!_)punct(_+)(?!_)(?=punct)",
  "gu"
).replace(/notPunctSpace/g, pt).replace(/punctSpace/g, qe).replace(/punct/g, _e).getRegex(), Xt = w(/\\(punct)/, "gu").replace(/punct/g, _e).getRegex(), Jt = w(/^<(scheme:[^\s\x00-\x1f<>]*|email)>/).replace("scheme", /[a-zA-Z][a-zA-Z0-9+.-]{1,31}/).replace("email", /[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+(@)[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+(?![-_])/).getRegex(), Yt = w(De).replace("(?:-->|$)", "-->").getRegex(), Kt = w(
  "^comment|^</[a-zA-Z][\\w:-]*\\s*>|^<[a-zA-Z][\\w-]*(?:attribute)*?\\s*/?>|^<\\?[\\s\\S]*?\\?>|^<![a-zA-Z]+\\s[\\s\\S]*?>|^<!\\[CDATA\\[[\\s\\S]*?\\]\\]>"
).replace("comment", Yt).replace("attribute", /\s+[a-zA-Z:_][\w.:-]*(?:\s*=\s*"[^"]*"|\s*=\s*'[^']*'|\s*=\s*[^\s"'=<>`]+)?/).getRegex(), be = /(?:\[(?:\\.|[^\[\]\\])*\]|\\.|`[^`]*`|[^\[\]\\`])*?/, en = w(/^!?\[(label)\]\(\s*(href)(?:(?:[ \t]*(?:\n[ \t]*)?)(title))?\s*\)/).replace("label", be).replace("href", /<(?:\\.|[^\n<>\\])+>|[^ \t\n\x00-\x1f]*/).replace("title", /"(?:\\"?|[^"\\])*"|'(?:\\'?|[^'\\])*'|\((?:\\\)?|[^)\\])*\)/).getRegex(), kt = w(/^!?\[(label)\]\[(ref)\]/).replace("label", be).replace("ref", Pe).getRegex(), mt = w(/^!?\[(ref)\](?:\[\])?/).replace("ref", Pe).getRegex(), tn = w("reflink|nolink(?!\\()", "g").replace("reflink", kt).replace("nolink", mt).getRegex(), Ne = {
  _backpedal: ae,
  // only used for GFM url
  anyPunctuation: Xt,
  autolink: Jt,
  blockSkip: Ft,
  br: ht,
  code: Ot,
  del: ae,
  emStrongLDelim: Qt,
  emStrongRDelimAst: jt,
  emStrongRDelimUnd: Ut,
  escape: Nt,
  link: en,
  nolink: mt,
  punctuation: Mt,
  reflink: kt,
  reflinkSearch: tn,
  tag: Kt,
  text: Zt,
  url: ae
}, nn = {
  ...Ne,
  link: w(/^!?\[(label)\]\((.*?)\)/).replace("label", be).getRegex(),
  reflink: w(/^!?\[(label)\]\s*\[([^\]]*)\]/).replace("label", be).getRegex()
}, Se = {
  ...Ne,
  emStrongRDelimAst: Wt,
  emStrongLDelim: Vt,
  url: w(/^((?:ftp|https?):\/\/|www\.)(?:[a-zA-Z0-9\-]+\.?)+[^\s<]*|^email/, "i").replace("email", /[A-Za-z0-9._+-]+(@)[a-zA-Z0-9-_]+(?:\.[a-zA-Z0-9-_]*[a-zA-Z0-9])+(?![-_])/).getRegex(),
  _backpedal: /(?:[^?!.,:;*_'"~()&]+|\([^)]*\)|&(?![a-zA-Z0-9]+;$)|[?!.,:;*_'"~)]+(?!$))+/,
  del: /^(~~?)(?=[^\s~])((?:\\.|[^\\])*?(?:\\.|[^\s~\\]))\1(?=[^~]|$)/,
  text: /^([`~]+|[^`~])(?:(?= {2,}\n)|(?=[a-zA-Z0-9.!#$%&'*+\/=?_`{\|}~-]+@)|[\s\S]*?(?:(?=[\\<!\[`*~_]|\b_|https?:\/\/|ftp:\/\/|www\.|$)|[^ ](?= {2,}\n)|[^a-zA-Z0-9.!#$%&'*+\/=?_`{\|}~-](?=[a-zA-Z0-9.!#$%&'*+\/=?_`{\|}~-]+@)))/
}, sn = {
  ...Se,
  br: w(ht).replace("{2,}", "*").getRegex(),
  text: w(Se.text).replace("\\b_", "\\b_| {2,}\\n").replace(/\{2,\}/g, "*").getRegex()
}, de = {
  normal: Be,
  gfm: Bt,
  pedantic: qt
}, re = {
  normal: Ne,
  gfm: Se,
  breaks: sn,
  pedantic: nn
}, rn = {
  "&": "&amp;",
  "<": "&lt;",
  ">": "&gt;",
  '"': "&quot;",
  "'": "&#39;"
}, Ue = (n) => rn[n];
function M(n, e) {
  if (e) {
    if (P.escapeTest.test(n))
      return n.replace(P.escapeReplace, Ue);
  } else if (P.escapeTestNoEncode.test(n))
    return n.replace(P.escapeReplaceNoEncode, Ue);
  return n;
}
function Xe(n) {
  try {
    n = encodeURI(n).replace(P.percentDecode, "%");
  } catch {
    return null;
  }
  return n;
}
function Je(n, e) {
  var r;
  const t = n.replace(P.findPipe, (c, l, u) => {
    let a = !1, o = l;
    for (; --o >= 0 && u[o] === "\\"; ) a = !a;
    return a ? "|" : " |";
  }), s = t.split(P.splitPipe);
  let i = 0;
  if (s[0].trim() || s.shift(), s.length > 0 && !((r = s.at(-1)) != null && r.trim()) && s.pop(), e)
    if (s.length > e)
      s.splice(e);
    else
      for (; s.length < e; ) s.push("");
  for (; i < s.length; i++)
    s[i] = s[i].trim().replace(P.slashPipe, "|");
  return s;
}
function le(n, e, t) {
  const s = n.length;
  if (s === 0)
    return "";
  let i = 0;
  for (; i < s && n.charAt(s - i - 1) === e; )
    i++;
  return n.slice(0, s - i);
}
function ln(n, e) {
  if (n.indexOf(e[1]) === -1)
    return -1;
  let t = 0;
  for (let s = 0; s < n.length; s++)
    if (n[s] === "\\")
      s++;
    else if (n[s] === e[0])
      t++;
    else if (n[s] === e[1] && (t--, t < 0))
      return s;
  return t > 0 ? -2 : -1;
}
function Ye(n, e, t, s, i) {
  const r = e.href, c = e.title || null, l = n[1].replace(i.other.outputLinkReplace, "$1");
  s.state.inLink = !0;
  const u = {
    type: n[0].charAt(0) === "!" ? "image" : "link",
    raw: t,
    href: r,
    title: c,
    text: l,
    tokens: s.inlineTokens(l)
  };
  return s.state.inLink = !1, u;
}
function an(n, e, t) {
  const s = n.match(t.other.indentCodeCompensation);
  if (s === null)
    return e;
  const i = s[1];
  return e.split(`
`).map((r) => {
    const c = r.match(t.other.beginningSpace);
    if (c === null)
      return r;
    const [l] = c;
    return l.length >= i.length ? r.slice(i.length) : r;
  }).join(`
`);
}
var xe = class {
  // set by the lexer
  constructor(n) {
    v(this, "options");
    v(this, "rules");
    // set by the lexer
    v(this, "lexer");
    this.options = n || X;
  }
  space(n) {
    const e = this.rules.block.newline.exec(n);
    if (e && e[0].length > 0)
      return {
        type: "space",
        raw: e[0]
      };
  }
  code(n) {
    const e = this.rules.block.code.exec(n);
    if (e) {
      const t = e[0].replace(this.rules.other.codeRemoveIndent, "");
      return {
        type: "code",
        raw: e[0],
        codeBlockStyle: "indented",
        text: this.options.pedantic ? t : le(t, `
`)
      };
    }
  }
  fences(n) {
    const e = this.rules.block.fences.exec(n);
    if (e) {
      const t = e[0], s = an(t, e[3] || "", this.rules);
      return {
        type: "code",
        raw: t,
        lang: e[2] ? e[2].trim().replace(this.rules.inline.anyPunctuation, "$1") : e[2],
        text: s
      };
    }
  }
  heading(n) {
    const e = this.rules.block.heading.exec(n);
    if (e) {
      let t = e[2].trim();
      if (this.rules.other.endingHash.test(t)) {
        const s = le(t, "#");
        (this.options.pedantic || !s || this.rules.other.endingSpaceChar.test(s)) && (t = s.trim());
      }
      return {
        type: "heading",
        raw: e[0],
        depth: e[1].length,
        text: t,
        tokens: this.lexer.inline(t)
      };
    }
  }
  hr(n) {
    const e = this.rules.block.hr.exec(n);
    if (e)
      return {
        type: "hr",
        raw: le(e[0], `
`)
      };
  }
  blockquote(n) {
    const e = this.rules.block.blockquote.exec(n);
    if (e) {
      let t = le(e[0], `
`).split(`
`), s = "", i = "";
      const r = [];
      for (; t.length > 0; ) {
        let c = !1;
        const l = [];
        let u;
        for (u = 0; u < t.length; u++)
          if (this.rules.other.blockquoteStart.test(t[u]))
            l.push(t[u]), c = !0;
          else if (!c)
            l.push(t[u]);
          else
            break;
        t = t.slice(u);
        const a = l.join(`
`), o = a.replace(this.rules.other.blockquoteSetextReplace, `
    $1`).replace(this.rules.other.blockquoteSetextReplace2, "");
        s = s ? `${s}
${a}` : a, i = i ? `${i}
${o}` : o;
        const p = this.lexer.state.top;
        if (this.lexer.state.top = !0, this.lexer.blockTokens(o, r, !0), this.lexer.state.top = p, t.length === 0)
          break;
        const h = r.at(-1);
        if ((h == null ? void 0 : h.type) === "code")
          break;
        if ((h == null ? void 0 : h.type) === "blockquote") {
          const d = h, f = d.raw + `
` + t.join(`
`), k = this.blockquote(f);
          r[r.length - 1] = k, s = s.substring(0, s.length - d.raw.length) + k.raw, i = i.substring(0, i.length - d.text.length) + k.text;
          break;
        } else if ((h == null ? void 0 : h.type) === "list") {
          const d = h, f = d.raw + `
` + t.join(`
`), k = this.list(f);
          r[r.length - 1] = k, s = s.substring(0, s.length - h.raw.length) + k.raw, i = i.substring(0, i.length - d.raw.length) + k.raw, t = f.substring(r.at(-1).raw.length).split(`
`);
          continue;
        }
      }
      return {
        type: "blockquote",
        raw: s,
        tokens: r,
        text: i
      };
    }
  }
  list(n) {
    let e = this.rules.block.list.exec(n);
    if (e) {
      let t = e[1].trim();
      const s = t.length > 1, i = {
        type: "list",
        raw: "",
        ordered: s,
        start: s ? +t.slice(0, -1) : "",
        loose: !1,
        items: []
      };
      t = s ? `\\d{1,9}\\${t.slice(-1)}` : `\\${t}`, this.options.pedantic && (t = s ? t : "[*+-]");
      const r = this.rules.other.listItemRegex(t);
      let c = !1;
      for (; n; ) {
        let u = !1, a = "", o = "";
        if (!(e = r.exec(n)) || this.rules.block.hr.test(n))
          break;
        a = e[0], n = n.substring(a.length);
        let p = e[2].split(`
`, 1)[0].replace(this.rules.other.listReplaceTabs, (I) => " ".repeat(3 * I.length)), h = n.split(`
`, 1)[0], d = !p.trim(), f = 0;
        if (this.options.pedantic ? (f = 2, o = p.trimStart()) : d ? f = e[1].length + 1 : (f = e[2].search(this.rules.other.nonSpaceChar), f = f > 4 ? 1 : f, o = p.slice(f), f += e[1].length), d && this.rules.other.blankLine.test(h) && (a += h + `
`, n = n.substring(h.length + 1), u = !0), !u) {
          const I = this.rules.other.nextBulletRegex(f), E = this.rules.other.hrRegex(f), B = this.rules.other.fencesBeginRegex(f), R = this.rules.other.headingBeginRegex(f), q = this.rules.other.htmlBeginRegex(f);
          for (; n; ) {
            const $ = n.split(`
`, 1)[0];
            let z;
            if (h = $, this.options.pedantic ? (h = h.replace(this.rules.other.listReplaceNesting, "  "), z = h) : z = h.replace(this.rules.other.tabCharGlobal, "    "), B.test(h) || R.test(h) || q.test(h) || I.test(h) || E.test(h))
              break;
            if (z.search(this.rules.other.nonSpaceChar) >= f || !h.trim())
              o += `
` + z.slice(f);
            else {
              if (d || p.replace(this.rules.other.tabCharGlobal, "    ").search(this.rules.other.nonSpaceChar) >= 4 || B.test(p) || R.test(p) || E.test(p))
                break;
              o += `
` + h;
            }
            !d && !h.trim() && (d = !0), a += $ + `
`, n = n.substring($.length + 1), p = z.slice(f);
          }
        }
        i.loose || (c ? i.loose = !0 : this.rules.other.doubleBlankLine.test(a) && (c = !0));
        let k = null, g;
        this.options.gfm && (k = this.rules.other.listIsTask.exec(o), k && (g = k[0] !== "[ ] ", o = o.replace(this.rules.other.listReplaceTask, ""))), i.items.push({
          type: "list_item",
          raw: a,
          task: !!k,
          checked: g,
          loose: !1,
          text: o,
          tokens: []
        }), i.raw += a;
      }
      const l = i.items.at(-1);
      if (l)
        l.raw = l.raw.trimEnd(), l.text = l.text.trimEnd();
      else
        return;
      i.raw = i.raw.trimEnd();
      for (let u = 0; u < i.items.length; u++)
        if (this.lexer.state.top = !1, i.items[u].tokens = this.lexer.blockTokens(i.items[u].text, []), !i.loose) {
          const a = i.items[u].tokens.filter((p) => p.type === "space"), o = a.length > 0 && a.some((p) => this.rules.other.anyLine.test(p.raw));
          i.loose = o;
        }
      if (i.loose)
        for (let u = 0; u < i.items.length; u++)
          i.items[u].loose = !0;
      return i;
    }
  }
  html(n) {
    const e = this.rules.block.html.exec(n);
    if (e)
      return {
        type: "html",
        block: !0,
        raw: e[0],
        pre: e[1] === "pre" || e[1] === "script" || e[1] === "style",
        text: e[0]
      };
  }
  def(n) {
    const e = this.rules.block.def.exec(n);
    if (e) {
      const t = e[1].toLowerCase().replace(this.rules.other.multipleSpaceGlobal, " "), s = e[2] ? e[2].replace(this.rules.other.hrefBrackets, "$1").replace(this.rules.inline.anyPunctuation, "$1") : "", i = e[3] ? e[3].substring(1, e[3].length - 1).replace(this.rules.inline.anyPunctuation, "$1") : e[3];
      return {
        type: "def",
        tag: t,
        raw: e[0],
        href: s,
        title: i
      };
    }
  }
  table(n) {
    var c;
    const e = this.rules.block.table.exec(n);
    if (!e || !this.rules.other.tableDelimiter.test(e[2]))
      return;
    const t = Je(e[1]), s = e[2].replace(this.rules.other.tableAlignChars, "").split("|"), i = (c = e[3]) != null && c.trim() ? e[3].replace(this.rules.other.tableRowBlankLine, "").split(`
`) : [], r = {
      type: "table",
      raw: e[0],
      header: [],
      align: [],
      rows: []
    };
    if (t.length === s.length) {
      for (const l of s)
        this.rules.other.tableAlignRight.test(l) ? r.align.push("right") : this.rules.other.tableAlignCenter.test(l) ? r.align.push("center") : this.rules.other.tableAlignLeft.test(l) ? r.align.push("left") : r.align.push(null);
      for (let l = 0; l < t.length; l++)
        r.header.push({
          text: t[l],
          tokens: this.lexer.inline(t[l]),
          header: !0,
          align: r.align[l]
        });
      for (const l of i)
        r.rows.push(Je(l, r.header.length).map((u, a) => ({
          text: u,
          tokens: this.lexer.inline(u),
          header: !1,
          align: r.align[a]
        })));
      return r;
    }
  }
  lheading(n) {
    const e = this.rules.block.lheading.exec(n);
    if (e)
      return {
        type: "heading",
        raw: e[0],
        depth: e[2].charAt(0) === "=" ? 1 : 2,
        text: e[1],
        tokens: this.lexer.inline(e[1])
      };
  }
  paragraph(n) {
    const e = this.rules.block.paragraph.exec(n);
    if (e) {
      const t = e[1].charAt(e[1].length - 1) === `
` ? e[1].slice(0, -1) : e[1];
      return {
        type: "paragraph",
        raw: e[0],
        text: t,
        tokens: this.lexer.inline(t)
      };
    }
  }
  text(n) {
    const e = this.rules.block.text.exec(n);
    if (e)
      return {
        type: "text",
        raw: e[0],
        text: e[0],
        tokens: this.lexer.inline(e[0])
      };
  }
  escape(n) {
    const e = this.rules.inline.escape.exec(n);
    if (e)
      return {
        type: "escape",
        raw: e[0],
        text: e[1]
      };
  }
  tag(n) {
    const e = this.rules.inline.tag.exec(n);
    if (e)
      return !this.lexer.state.inLink && this.rules.other.startATag.test(e[0]) ? this.lexer.state.inLink = !0 : this.lexer.state.inLink && this.rules.other.endATag.test(e[0]) && (this.lexer.state.inLink = !1), !this.lexer.state.inRawBlock && this.rules.other.startPreScriptTag.test(e[0]) ? this.lexer.state.inRawBlock = !0 : this.lexer.state.inRawBlock && this.rules.other.endPreScriptTag.test(e[0]) && (this.lexer.state.inRawBlock = !1), {
        type: "html",
        raw: e[0],
        inLink: this.lexer.state.inLink,
        inRawBlock: this.lexer.state.inRawBlock,
        block: !1,
        text: e[0]
      };
  }
  link(n) {
    const e = this.rules.inline.link.exec(n);
    if (e) {
      const t = e[2].trim();
      if (!this.options.pedantic && this.rules.other.startAngleBracket.test(t)) {
        if (!this.rules.other.endAngleBracket.test(t))
          return;
        const r = le(t.slice(0, -1), "\\");
        if ((t.length - r.length) % 2 === 0)
          return;
      } else {
        const r = ln(e[2], "()");
        if (r === -2)
          return;
        if (r > -1) {
          const l = (e[0].indexOf("!") === 0 ? 5 : 4) + e[1].length + r;
          e[2] = e[2].substring(0, r), e[0] = e[0].substring(0, l).trim(), e[3] = "";
        }
      }
      let s = e[2], i = "";
      if (this.options.pedantic) {
        const r = this.rules.other.pedanticHrefTitle.exec(s);
        r && (s = r[1], i = r[3]);
      } else
        i = e[3] ? e[3].slice(1, -1) : "";
      return s = s.trim(), this.rules.other.startAngleBracket.test(s) && (this.options.pedantic && !this.rules.other.endAngleBracket.test(t) ? s = s.slice(1) : s = s.slice(1, -1)), Ye(e, {
        href: s && s.replace(this.rules.inline.anyPunctuation, "$1"),
        title: i && i.replace(this.rules.inline.anyPunctuation, "$1")
      }, e[0], this.lexer, this.rules);
    }
  }
  reflink(n, e) {
    let t;
    if ((t = this.rules.inline.reflink.exec(n)) || (t = this.rules.inline.nolink.exec(n))) {
      const s = (t[2] || t[1]).replace(this.rules.other.multipleSpaceGlobal, " "), i = e[s.toLowerCase()];
      if (!i) {
        const r = t[0].charAt(0);
        return {
          type: "text",
          raw: r,
          text: r
        };
      }
      return Ye(t, i, t[0], this.lexer, this.rules);
    }
  }
  emStrong(n, e, t = "") {
    let s = this.rules.inline.emStrongLDelim.exec(n);
    if (!s || s[3] && t.match(this.rules.other.unicodeAlphaNumeric)) return;
    if (!(s[1] || s[2] || "") || !t || this.rules.inline.punctuation.exec(t)) {
      const r = [...s[0]].length - 1;
      let c, l, u = r, a = 0;
      const o = s[0][0] === "*" ? this.rules.inline.emStrongRDelimAst : this.rules.inline.emStrongRDelimUnd;
      for (o.lastIndex = 0, e = e.slice(-1 * n.length + r); (s = o.exec(e)) != null; ) {
        if (c = s[1] || s[2] || s[3] || s[4] || s[5] || s[6], !c) continue;
        if (l = [...c].length, s[3] || s[4]) {
          u += l;
          continue;
        } else if ((s[5] || s[6]) && r % 3 && !((r + l) % 3)) {
          a += l;
          continue;
        }
        if (u -= l, u > 0) continue;
        l = Math.min(l, l + u + a);
        const p = [...s[0]][0].length, h = n.slice(0, r + s.index + p + l);
        if (Math.min(r, l) % 2) {
          const f = h.slice(1, -1);
          return {
            type: "em",
            raw: h,
            text: f,
            tokens: this.lexer.inlineTokens(f)
          };
        }
        const d = h.slice(2, -2);
        return {
          type: "strong",
          raw: h,
          text: d,
          tokens: this.lexer.inlineTokens(d)
        };
      }
    }
  }
  codespan(n) {
    const e = this.rules.inline.code.exec(n);
    if (e) {
      let t = e[2].replace(this.rules.other.newLineCharGlobal, " ");
      const s = this.rules.other.nonSpaceChar.test(t), i = this.rules.other.startingSpaceChar.test(t) && this.rules.other.endingSpaceChar.test(t);
      return s && i && (t = t.substring(1, t.length - 1)), {
        type: "codespan",
        raw: e[0],
        text: t
      };
    }
  }
  br(n) {
    const e = this.rules.inline.br.exec(n);
    if (e)
      return {
        type: "br",
        raw: e[0]
      };
  }
  del(n) {
    const e = this.rules.inline.del.exec(n);
    if (e)
      return {
        type: "del",
        raw: e[0],
        text: e[2],
        tokens: this.lexer.inlineTokens(e[2])
      };
  }
  autolink(n) {
    const e = this.rules.inline.autolink.exec(n);
    if (e) {
      let t, s;
      return e[2] === "@" ? (t = e[1], s = "mailto:" + t) : (t = e[1], s = t), {
        type: "link",
        raw: e[0],
        text: t,
        href: s,
        tokens: [
          {
            type: "text",
            raw: t,
            text: t
          }
        ]
      };
    }
  }
  url(n) {
    var t;
    let e;
    if (e = this.rules.inline.url.exec(n)) {
      let s, i;
      if (e[2] === "@")
        s = e[0], i = "mailto:" + s;
      else {
        let r;
        do
          r = e[0], e[0] = ((t = this.rules.inline._backpedal.exec(e[0])) == null ? void 0 : t[0]) ?? "";
        while (r !== e[0]);
        s = e[0], e[1] === "www." ? i = "http://" + e[0] : i = e[0];
      }
      return {
        type: "link",
        raw: e[0],
        text: s,
        href: i,
        tokens: [
          {
            type: "text",
            raw: s,
            text: s
          }
        ]
      };
    }
  }
  inlineText(n) {
    const e = this.rules.inline.text.exec(n);
    if (e) {
      const t = this.lexer.state.inRawBlock;
      return {
        type: "text",
        raw: e[0],
        text: e[0],
        escaped: t
      };
    }
  }
}, F = class ze {
  constructor(e) {
    v(this, "tokens");
    v(this, "options");
    v(this, "state");
    v(this, "tokenizer");
    v(this, "inlineQueue");
    this.tokens = [], this.tokens.links = /* @__PURE__ */ Object.create(null), this.options = e || X, this.options.tokenizer = this.options.tokenizer || new xe(), this.tokenizer = this.options.tokenizer, this.tokenizer.options = this.options, this.tokenizer.lexer = this, this.inlineQueue = [], this.state = {
      inLink: !1,
      inRawBlock: !1,
      top: !0
    };
    const t = {
      other: P,
      block: de.normal,
      inline: re.normal
    };
    this.options.pedantic ? (t.block = de.pedantic, t.inline = re.pedantic) : this.options.gfm && (t.block = de.gfm, this.options.breaks ? t.inline = re.breaks : t.inline = re.gfm), this.tokenizer.rules = t;
  }
  /**
   * Expose Rules
   */
  static get rules() {
    return {
      block: de,
      inline: re
    };
  }
  /**
   * Static Lex Method
   */
  static lex(e, t) {
    return new ze(t).lex(e);
  }
  /**
   * Static Lex Inline Method
   */
  static lexInline(e, t) {
    return new ze(t).inlineTokens(e);
  }
  /**
   * Preprocessing
   */
  lex(e) {
    e = e.replace(P.carriageReturn, `
`), this.blockTokens(e, this.tokens);
    for (let t = 0; t < this.inlineQueue.length; t++) {
      const s = this.inlineQueue[t];
      this.inlineTokens(s.src, s.tokens);
    }
    return this.inlineQueue = [], this.tokens;
  }
  blockTokens(e, t = [], s = !1) {
    var i, r, c;
    for (this.options.pedantic && (e = e.replace(P.tabCharGlobal, "    ").replace(P.spaceLine, "")); e; ) {
      let l;
      if ((r = (i = this.options.extensions) == null ? void 0 : i.block) != null && r.some((a) => (l = a.call({ lexer: this }, e, t)) ? (e = e.substring(l.raw.length), t.push(l), !0) : !1))
        continue;
      if (l = this.tokenizer.space(e)) {
        e = e.substring(l.raw.length);
        const a = t.at(-1);
        l.raw.length === 1 && a !== void 0 ? a.raw += `
` : t.push(l);
        continue;
      }
      if (l = this.tokenizer.code(e)) {
        e = e.substring(l.raw.length);
        const a = t.at(-1);
        (a == null ? void 0 : a.type) === "paragraph" || (a == null ? void 0 : a.type) === "text" ? (a.raw += `
` + l.raw, a.text += `
` + l.text, this.inlineQueue.at(-1).src = a.text) : t.push(l);
        continue;
      }
      if (l = this.tokenizer.fences(e)) {
        e = e.substring(l.raw.length), t.push(l);
        continue;
      }
      if (l = this.tokenizer.heading(e)) {
        e = e.substring(l.raw.length), t.push(l);
        continue;
      }
      if (l = this.tokenizer.hr(e)) {
        e = e.substring(l.raw.length), t.push(l);
        continue;
      }
      if (l = this.tokenizer.blockquote(e)) {
        e = e.substring(l.raw.length), t.push(l);
        continue;
      }
      if (l = this.tokenizer.list(e)) {
        e = e.substring(l.raw.length), t.push(l);
        continue;
      }
      if (l = this.tokenizer.html(e)) {
        e = e.substring(l.raw.length), t.push(l);
        continue;
      }
      if (l = this.tokenizer.def(e)) {
        e = e.substring(l.raw.length);
        const a = t.at(-1);
        (a == null ? void 0 : a.type) === "paragraph" || (a == null ? void 0 : a.type) === "text" ? (a.raw += `
` + l.raw, a.text += `
` + l.raw, this.inlineQueue.at(-1).src = a.text) : this.tokens.links[l.tag] || (this.tokens.links[l.tag] = {
          href: l.href,
          title: l.title
        });
        continue;
      }
      if (l = this.tokenizer.table(e)) {
        e = e.substring(l.raw.length), t.push(l);
        continue;
      }
      if (l = this.tokenizer.lheading(e)) {
        e = e.substring(l.raw.length), t.push(l);
        continue;
      }
      let u = e;
      if ((c = this.options.extensions) != null && c.startBlock) {
        let a = 1 / 0;
        const o = e.slice(1);
        let p;
        this.options.extensions.startBlock.forEach((h) => {
          p = h.call({ lexer: this }, o), typeof p == "number" && p >= 0 && (a = Math.min(a, p));
        }), a < 1 / 0 && a >= 0 && (u = e.substring(0, a + 1));
      }
      if (this.state.top && (l = this.tokenizer.paragraph(u))) {
        const a = t.at(-1);
        s && (a == null ? void 0 : a.type) === "paragraph" ? (a.raw += `
` + l.raw, a.text += `
` + l.text, this.inlineQueue.pop(), this.inlineQueue.at(-1).src = a.text) : t.push(l), s = u.length !== e.length, e = e.substring(l.raw.length);
        continue;
      }
      if (l = this.tokenizer.text(e)) {
        e = e.substring(l.raw.length);
        const a = t.at(-1);
        (a == null ? void 0 : a.type) === "text" ? (a.raw += `
` + l.raw, a.text += `
` + l.text, this.inlineQueue.pop(), this.inlineQueue.at(-1).src = a.text) : t.push(l);
        continue;
      }
      if (e) {
        const a = "Infinite loop on byte: " + e.charCodeAt(0);
        if (this.options.silent) {
          console.error(a);
          break;
        } else
          throw new Error(a);
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
    var l, u, a;
    let s = e, i = null;
    if (this.tokens.links) {
      const o = Object.keys(this.tokens.links);
      if (o.length > 0)
        for (; (i = this.tokenizer.rules.inline.reflinkSearch.exec(s)) != null; )
          o.includes(i[0].slice(i[0].lastIndexOf("[") + 1, -1)) && (s = s.slice(0, i.index) + "[" + "a".repeat(i[0].length - 2) + "]" + s.slice(this.tokenizer.rules.inline.reflinkSearch.lastIndex));
    }
    for (; (i = this.tokenizer.rules.inline.anyPunctuation.exec(s)) != null; )
      s = s.slice(0, i.index) + "++" + s.slice(this.tokenizer.rules.inline.anyPunctuation.lastIndex);
    for (; (i = this.tokenizer.rules.inline.blockSkip.exec(s)) != null; )
      s = s.slice(0, i.index) + "[" + "a".repeat(i[0].length - 2) + "]" + s.slice(this.tokenizer.rules.inline.blockSkip.lastIndex);
    let r = !1, c = "";
    for (; e; ) {
      r || (c = ""), r = !1;
      let o;
      if ((u = (l = this.options.extensions) == null ? void 0 : l.inline) != null && u.some((h) => (o = h.call({ lexer: this }, e, t)) ? (e = e.substring(o.raw.length), t.push(o), !0) : !1))
        continue;
      if (o = this.tokenizer.escape(e)) {
        e = e.substring(o.raw.length), t.push(o);
        continue;
      }
      if (o = this.tokenizer.tag(e)) {
        e = e.substring(o.raw.length), t.push(o);
        continue;
      }
      if (o = this.tokenizer.link(e)) {
        e = e.substring(o.raw.length), t.push(o);
        continue;
      }
      if (o = this.tokenizer.reflink(e, this.tokens.links)) {
        e = e.substring(o.raw.length);
        const h = t.at(-1);
        o.type === "text" && (h == null ? void 0 : h.type) === "text" ? (h.raw += o.raw, h.text += o.text) : t.push(o);
        continue;
      }
      if (o = this.tokenizer.emStrong(e, s, c)) {
        e = e.substring(o.raw.length), t.push(o);
        continue;
      }
      if (o = this.tokenizer.codespan(e)) {
        e = e.substring(o.raw.length), t.push(o);
        continue;
      }
      if (o = this.tokenizer.br(e)) {
        e = e.substring(o.raw.length), t.push(o);
        continue;
      }
      if (o = this.tokenizer.del(e)) {
        e = e.substring(o.raw.length), t.push(o);
        continue;
      }
      if (o = this.tokenizer.autolink(e)) {
        e = e.substring(o.raw.length), t.push(o);
        continue;
      }
      if (!this.state.inLink && (o = this.tokenizer.url(e))) {
        e = e.substring(o.raw.length), t.push(o);
        continue;
      }
      let p = e;
      if ((a = this.options.extensions) != null && a.startInline) {
        let h = 1 / 0;
        const d = e.slice(1);
        let f;
        this.options.extensions.startInline.forEach((k) => {
          f = k.call({ lexer: this }, d), typeof f == "number" && f >= 0 && (h = Math.min(h, f));
        }), h < 1 / 0 && h >= 0 && (p = e.substring(0, h + 1));
      }
      if (o = this.tokenizer.inlineText(p)) {
        e = e.substring(o.raw.length), o.raw.slice(-1) !== "_" && (c = o.raw.slice(-1)), r = !0;
        const h = t.at(-1);
        (h == null ? void 0 : h.type) === "text" ? (h.raw += o.raw, h.text += o.text) : t.push(o);
        continue;
      }
      if (e) {
        const h = "Infinite loop on byte: " + e.charCodeAt(0);
        if (this.options.silent) {
          console.error(h);
          break;
        } else
          throw new Error(h);
      }
    }
    return t;
  }
}, we = class {
  // set by the parser
  constructor(n) {
    v(this, "options");
    v(this, "parser");
    this.options = n || X;
  }
  space(n) {
    return "";
  }
  code({ text: n, lang: e, escaped: t }) {
    var r;
    const s = (r = (e || "").match(P.notSpaceStart)) == null ? void 0 : r[0], i = n.replace(P.endingNewline, "") + `
`;
    return s ? '<pre><code class="language-' + M(s) + '">' + (t ? i : M(i, !0)) + `</code></pre>
` : "<pre><code>" + (t ? i : M(i, !0)) + `</code></pre>
`;
  }
  blockquote({ tokens: n }) {
    return `<blockquote>
${this.parser.parse(n)}</blockquote>
`;
  }
  html({ text: n }) {
    return n;
  }
  heading({ tokens: n, depth: e }) {
    return `<h${e}>${this.parser.parseInline(n)}</h${e}>
`;
  }
  hr(n) {
    return `<hr>
`;
  }
  list(n) {
    const e = n.ordered, t = n.start;
    let s = "";
    for (let c = 0; c < n.items.length; c++) {
      const l = n.items[c];
      s += this.listitem(l);
    }
    const i = e ? "ol" : "ul", r = e && t !== 1 ? ' start="' + t + '"' : "";
    return "<" + i + r + `>
` + s + "</" + i + `>
`;
  }
  listitem(n) {
    var t;
    let e = "";
    if (n.task) {
      const s = this.checkbox({ checked: !!n.checked });
      n.loose ? ((t = n.tokens[0]) == null ? void 0 : t.type) === "paragraph" ? (n.tokens[0].text = s + " " + n.tokens[0].text, n.tokens[0].tokens && n.tokens[0].tokens.length > 0 && n.tokens[0].tokens[0].type === "text" && (n.tokens[0].tokens[0].text = s + " " + M(n.tokens[0].tokens[0].text), n.tokens[0].tokens[0].escaped = !0)) : n.tokens.unshift({
        type: "text",
        raw: s + " ",
        text: s + " ",
        escaped: !0
      }) : e += s + " ";
    }
    return e += this.parser.parse(n.tokens, !!n.loose), `<li>${e}</li>
`;
  }
  checkbox({ checked: n }) {
    return "<input " + (n ? 'checked="" ' : "") + 'disabled="" type="checkbox">';
  }
  paragraph({ tokens: n }) {
    return `<p>${this.parser.parseInline(n)}</p>
`;
  }
  table(n) {
    let e = "", t = "";
    for (let i = 0; i < n.header.length; i++)
      t += this.tablecell(n.header[i]);
    e += this.tablerow({ text: t });
    let s = "";
    for (let i = 0; i < n.rows.length; i++) {
      const r = n.rows[i];
      t = "";
      for (let c = 0; c < r.length; c++)
        t += this.tablecell(r[c]);
      s += this.tablerow({ text: t });
    }
    return s && (s = `<tbody>${s}</tbody>`), `<table>
<thead>
` + e + `</thead>
` + s + `</table>
`;
  }
  tablerow({ text: n }) {
    return `<tr>
${n}</tr>
`;
  }
  tablecell(n) {
    const e = this.parser.parseInline(n.tokens), t = n.header ? "th" : "td";
    return (n.align ? `<${t} align="${n.align}">` : `<${t}>`) + e + `</${t}>
`;
  }
  /**
   * span level renderer
   */
  strong({ tokens: n }) {
    return `<strong>${this.parser.parseInline(n)}</strong>`;
  }
  em({ tokens: n }) {
    return `<em>${this.parser.parseInline(n)}</em>`;
  }
  codespan({ text: n }) {
    return `<code>${M(n, !0)}</code>`;
  }
  br(n) {
    return "<br>";
  }
  del({ tokens: n }) {
    return `<del>${this.parser.parseInline(n)}</del>`;
  }
  link({ href: n, title: e, tokens: t }) {
    const s = this.parser.parseInline(t), i = Xe(n);
    if (i === null)
      return s;
    n = i;
    let r = '<a href="' + n + '"';
    return e && (r += ' title="' + M(e) + '"'), r += ">" + s + "</a>", r;
  }
  image({ href: n, title: e, text: t, tokens: s }) {
    s && (t = this.parser.parseInline(s, this.parser.textRenderer));
    const i = Xe(n);
    if (i === null)
      return M(t);
    n = i;
    let r = `<img src="${n}" alt="${t}"`;
    return e && (r += ` title="${M(e)}"`), r += ">", r;
  }
  text(n) {
    return "tokens" in n && n.tokens ? this.parser.parseInline(n.tokens) : "escaped" in n && n.escaped ? n.text : M(n.text);
  }
}, Oe = class {
  // no need for block level renderers
  strong({ text: n }) {
    return n;
  }
  em({ text: n }) {
    return n;
  }
  codespan({ text: n }) {
    return n;
  }
  del({ text: n }) {
    return n;
  }
  html({ text: n }) {
    return n;
  }
  text({ text: n }) {
    return n;
  }
  link({ text: n }) {
    return "" + n;
  }
  image({ text: n }) {
    return "" + n;
  }
  br() {
    return "";
  }
}, Q = class $e {
  constructor(e) {
    v(this, "options");
    v(this, "renderer");
    v(this, "textRenderer");
    this.options = e || X, this.options.renderer = this.options.renderer || new we(), this.renderer = this.options.renderer, this.renderer.options = this.options, this.renderer.parser = this, this.textRenderer = new Oe();
  }
  /**
   * Static Parse Method
   */
  static parse(e, t) {
    return new $e(t).parse(e);
  }
  /**
   * Static Parse Inline Method
   */
  static parseInline(e, t) {
    return new $e(t).parseInline(e);
  }
  /**
   * Parse Loop
   */
  parse(e, t = !0) {
    var i, r;
    let s = "";
    for (let c = 0; c < e.length; c++) {
      const l = e[c];
      if ((r = (i = this.options.extensions) == null ? void 0 : i.renderers) != null && r[l.type]) {
        const a = l, o = this.options.extensions.renderers[a.type].call({ parser: this }, a);
        if (o !== !1 || !["space", "hr", "heading", "code", "table", "blockquote", "list", "html", "paragraph", "text"].includes(a.type)) {
          s += o || "";
          continue;
        }
      }
      const u = l;
      switch (u.type) {
        case "space": {
          s += this.renderer.space(u);
          continue;
        }
        case "hr": {
          s += this.renderer.hr(u);
          continue;
        }
        case "heading": {
          s += this.renderer.heading(u);
          continue;
        }
        case "code": {
          s += this.renderer.code(u);
          continue;
        }
        case "table": {
          s += this.renderer.table(u);
          continue;
        }
        case "blockquote": {
          s += this.renderer.blockquote(u);
          continue;
        }
        case "list": {
          s += this.renderer.list(u);
          continue;
        }
        case "html": {
          s += this.renderer.html(u);
          continue;
        }
        case "paragraph": {
          s += this.renderer.paragraph(u);
          continue;
        }
        case "text": {
          let a = u, o = this.renderer.text(a);
          for (; c + 1 < e.length && e[c + 1].type === "text"; )
            a = e[++c], o += `
` + this.renderer.text(a);
          t ? s += this.renderer.paragraph({
            type: "paragraph",
            raw: o,
            text: o,
            tokens: [{ type: "text", raw: o, text: o, escaped: !0 }]
          }) : s += o;
          continue;
        }
        default: {
          const a = 'Token with "' + u.type + '" type was not found.';
          if (this.options.silent)
            return console.error(a), "";
          throw new Error(a);
        }
      }
    }
    return s;
  }
  /**
   * Parse Inline Tokens
   */
  parseInline(e, t = this.renderer) {
    var i, r;
    let s = "";
    for (let c = 0; c < e.length; c++) {
      const l = e[c];
      if ((r = (i = this.options.extensions) == null ? void 0 : i.renderers) != null && r[l.type]) {
        const a = this.options.extensions.renderers[l.type].call({ parser: this }, l);
        if (a !== !1 || !["escape", "html", "link", "image", "strong", "em", "codespan", "br", "del", "text"].includes(l.type)) {
          s += a || "";
          continue;
        }
      }
      const u = l;
      switch (u.type) {
        case "escape": {
          s += t.text(u);
          break;
        }
        case "html": {
          s += t.html(u);
          break;
        }
        case "link": {
          s += t.link(u);
          break;
        }
        case "image": {
          s += t.image(u);
          break;
        }
        case "strong": {
          s += t.strong(u);
          break;
        }
        case "em": {
          s += t.em(u);
          break;
        }
        case "codespan": {
          s += t.codespan(u);
          break;
        }
        case "br": {
          s += t.br(u);
          break;
        }
        case "del": {
          s += t.del(u);
          break;
        }
        case "text": {
          s += t.text(u);
          break;
        }
        default: {
          const a = 'Token with "' + u.type + '" type was not found.';
          if (this.options.silent)
            return console.error(a), "";
          throw new Error(a);
        }
      }
    }
    return s;
  }
}, Re, me = (Re = class {
  constructor(n) {
    v(this, "options");
    v(this, "block");
    this.options = n || X;
  }
  /**
   * Process markdown before marked
   */
  preprocess(n) {
    return n;
  }
  /**
   * Process HTML after marked is finished
   */
  postprocess(n) {
    return n;
  }
  /**
   * Process all tokens before walk tokens
   */
  processAllTokens(n) {
    return n;
  }
  /**
   * Provide function to tokenize markdown
   */
  provideLexer() {
    return this.block ? F.lex : F.lexInline;
  }
  /**
   * Provide function to parse tokens
   */
  provideParser() {
    return this.block ? Q.parse : Q.parseInline;
  }
}, v(Re, "passThroughHooks", /* @__PURE__ */ new Set([
  "preprocess",
  "postprocess",
  "processAllTokens"
])), Re), on = class {
  constructor(...n) {
    v(this, "defaults", Le());
    v(this, "options", this.setOptions);
    v(this, "parse", this.parseMarkdown(!0));
    v(this, "parseInline", this.parseMarkdown(!1));
    v(this, "Parser", Q);
    v(this, "Renderer", we);
    v(this, "TextRenderer", Oe);
    v(this, "Lexer", F);
    v(this, "Tokenizer", xe);
    v(this, "Hooks", me);
    this.use(...n);
  }
  /**
   * Run callback for every token
   */
  walkTokens(n, e) {
    var s, i;
    let t = [];
    for (const r of n)
      switch (t = t.concat(e.call(this, r)), r.type) {
        case "table": {
          const c = r;
          for (const l of c.header)
            t = t.concat(this.walkTokens(l.tokens, e));
          for (const l of c.rows)
            for (const u of l)
              t = t.concat(this.walkTokens(u.tokens, e));
          break;
        }
        case "list": {
          const c = r;
          t = t.concat(this.walkTokens(c.items, e));
          break;
        }
        default: {
          const c = r;
          (i = (s = this.defaults.extensions) == null ? void 0 : s.childTokens) != null && i[c.type] ? this.defaults.extensions.childTokens[c.type].forEach((l) => {
            const u = c[l].flat(1 / 0);
            t = t.concat(this.walkTokens(u, e));
          }) : c.tokens && (t = t.concat(this.walkTokens(c.tokens, e)));
        }
      }
    return t;
  }
  use(...n) {
    const e = this.defaults.extensions || { renderers: {}, childTokens: {} };
    return n.forEach((t) => {
      const s = { ...t };
      if (s.async = this.defaults.async || s.async || !1, t.extensions && (t.extensions.forEach((i) => {
        if (!i.name)
          throw new Error("extension name required");
        if ("renderer" in i) {
          const r = e.renderers[i.name];
          r ? e.renderers[i.name] = function(...c) {
            let l = i.renderer.apply(this, c);
            return l === !1 && (l = r.apply(this, c)), l;
          } : e.renderers[i.name] = i.renderer;
        }
        if ("tokenizer" in i) {
          if (!i.level || i.level !== "block" && i.level !== "inline")
            throw new Error("extension level must be 'block' or 'inline'");
          const r = e[i.level];
          r ? r.unshift(i.tokenizer) : e[i.level] = [i.tokenizer], i.start && (i.level === "block" ? e.startBlock ? e.startBlock.push(i.start) : e.startBlock = [i.start] : i.level === "inline" && (e.startInline ? e.startInline.push(i.start) : e.startInline = [i.start]));
        }
        "childTokens" in i && i.childTokens && (e.childTokens[i.name] = i.childTokens);
      }), s.extensions = e), t.renderer) {
        const i = this.defaults.renderer || new we(this.defaults);
        for (const r in t.renderer) {
          if (!(r in i))
            throw new Error(`renderer '${r}' does not exist`);
          if (["options", "parser"].includes(r))
            continue;
          const c = r, l = t.renderer[c], u = i[c];
          i[c] = (...a) => {
            let o = l.apply(i, a);
            return o === !1 && (o = u.apply(i, a)), o || "";
          };
        }
        s.renderer = i;
      }
      if (t.tokenizer) {
        const i = this.defaults.tokenizer || new xe(this.defaults);
        for (const r in t.tokenizer) {
          if (!(r in i))
            throw new Error(`tokenizer '${r}' does not exist`);
          if (["options", "rules", "lexer"].includes(r))
            continue;
          const c = r, l = t.tokenizer[c], u = i[c];
          i[c] = (...a) => {
            let o = l.apply(i, a);
            return o === !1 && (o = u.apply(i, a)), o;
          };
        }
        s.tokenizer = i;
      }
      if (t.hooks) {
        const i = this.defaults.hooks || new me();
        for (const r in t.hooks) {
          if (!(r in i))
            throw new Error(`hook '${r}' does not exist`);
          if (["options", "block"].includes(r))
            continue;
          const c = r, l = t.hooks[c], u = i[c];
          me.passThroughHooks.has(r) ? i[c] = (a) => {
            if (this.defaults.async)
              return Promise.resolve(l.call(i, a)).then((p) => u.call(i, p));
            const o = l.call(i, a);
            return u.call(i, o);
          } : i[c] = (...a) => {
            let o = l.apply(i, a);
            return o === !1 && (o = u.apply(i, a)), o;
          };
        }
        s.hooks = i;
      }
      if (t.walkTokens) {
        const i = this.defaults.walkTokens, r = t.walkTokens;
        s.walkTokens = function(c) {
          let l = [];
          return l.push(r.call(this, c)), i && (l = l.concat(i.call(this, c))), l;
        };
      }
      this.defaults = { ...this.defaults, ...s };
    }), this;
  }
  setOptions(n) {
    return this.defaults = { ...this.defaults, ...n }, this;
  }
  lexer(n, e) {
    return F.lex(n, e ?? this.defaults);
  }
  parser(n, e) {
    return Q.parse(n, e ?? this.defaults);
  }
  parseMarkdown(n) {
    return (t, s) => {
      const i = { ...s }, r = { ...this.defaults, ...i }, c = this.onError(!!r.silent, !!r.async);
      if (this.defaults.async === !0 && i.async === !1)
        return c(new Error("marked(): The async option was set to true by an extension. Remove async: false from the parse options object to return a Promise."));
      if (typeof t > "u" || t === null)
        return c(new Error("marked(): input parameter is undefined or null"));
      if (typeof t != "string")
        return c(new Error("marked(): input parameter is of type " + Object.prototype.toString.call(t) + ", string expected"));
      r.hooks && (r.hooks.options = r, r.hooks.block = n);
      const l = r.hooks ? r.hooks.provideLexer() : n ? F.lex : F.lexInline, u = r.hooks ? r.hooks.provideParser() : n ? Q.parse : Q.parseInline;
      if (r.async)
        return Promise.resolve(r.hooks ? r.hooks.preprocess(t) : t).then((a) => l(a, r)).then((a) => r.hooks ? r.hooks.processAllTokens(a) : a).then((a) => r.walkTokens ? Promise.all(this.walkTokens(a, r.walkTokens)).then(() => a) : a).then((a) => u(a, r)).then((a) => r.hooks ? r.hooks.postprocess(a) : a).catch(c);
      try {
        r.hooks && (t = r.hooks.preprocess(t));
        let a = l(t, r);
        r.hooks && (a = r.hooks.processAllTokens(a)), r.walkTokens && this.walkTokens(a, r.walkTokens);
        let o = u(a, r);
        return r.hooks && (o = r.hooks.postprocess(o)), o;
      } catch (a) {
        return c(a);
      }
    };
  }
  onError(n, e) {
    return (t) => {
      if (t.message += `
Please report this to https://github.com/markedjs/marked.`, n) {
        const s = "<p>An error occurred:</p><pre>" + M(t.message + "", !0) + "</pre>";
        return e ? Promise.resolve(s) : s;
      }
      if (e)
        return Promise.reject(t);
      throw t;
    };
  }
}, U = new on();
function m(n, e) {
  return U.parse(n, e);
}
m.options = m.setOptions = function(n) {
  return U.setOptions(n), m.defaults = U.defaults, at(m.defaults), m;
};
m.getDefaults = Le;
m.defaults = X;
m.use = function(...n) {
  return U.use(...n), m.defaults = U.defaults, at(m.defaults), m;
};
m.walkTokens = function(n, e) {
  return U.walkTokens(n, e);
};
m.parseInline = U.parseInline;
m.Parser = Q;
m.parser = Q.parse;
m.Renderer = we;
m.TextRenderer = Oe;
m.Lexer = F;
m.lexer = F.lex;
m.Tokenizer = xe;
m.Hooks = me;
m.parse = m;
m.options;
m.setOptions;
m.use;
m.walkTokens;
m.parseInline;
Q.parse;
F.lex;
const {
  HtmlTagHydration: cn,
  SvelteComponent: un,
  append_hydration: _,
  attr: y,
  children: L,
  claim_element: C,
  claim_html_tag: hn,
  claim_space: N,
  claim_text: te,
  destroy_each: pn,
  detach: x,
  element: T,
  ensure_array_like: Ke,
  flush: Z,
  get_svelte_dataset: K,
  init: fn,
  insert_hydration: D,
  noop: Ae,
  safe_not_equal: dn,
  set_data: ne,
  set_style: ge,
  space: O,
  text: se,
  toggle_class: ee
} = window.__gradio__svelte__internal;
function et(n, e, t) {
  const s = n.slice();
  return s[13] = e[t], s;
}
function tt(n) {
  let e, t = (
    /*loading_status*/
    (n[7].status === "pending" ? "Loading..." : (
      /*loading_status*/
      n[7].message || ""
    )) + ""
  ), s;
  return {
    c() {
      e = T("div"), s = se(t), this.h();
    },
    l(i) {
      e = C(i, "DIV", { class: !0 });
      var r = L(e);
      s = te(r, t), r.forEach(x), this.h();
    },
    h() {
      y(e, "class", "status-message svelte-1stw26d"), ee(
        e,
        "error",
        /*loading_status*/
        n[7].status === "error"
      );
    },
    m(i, r) {
      D(i, e, r), _(e, s);
    },
    p(i, r) {
      r & /*loading_status*/
      128 && t !== (t = /*loading_status*/
      (i[7].status === "pending" ? "Loading..." : (
        /*loading_status*/
        i[7].message || ""
      )) + "") && ne(s, t), r & /*loading_status*/
      128 && ee(
        e,
        "error",
        /*loading_status*/
        i[7].status === "error"
      );
    },
    d(i) {
      i && x(e);
    }
  };
}
function nt(n) {
  let e, t;
  return {
    c() {
      e = T("div"), t = se(
        /*label*/
        n[0]
      ), this.h();
    },
    l(s) {
      e = C(s, "DIV", { class: !0 });
      var i = L(e);
      t = te(
        i,
        /*label*/
        n[0]
      ), i.forEach(x), this.h();
    },
    h() {
      y(e, "class", "gradio-label");
    },
    m(s, i) {
      D(s, e, i), _(e, t);
    },
    p(s, i) {
      i & /*label*/
      1 && ne(
        t,
        /*label*/
        s[0]
      );
    },
    d(s) {
      s && x(e);
    }
  };
}
function gn(n) {
  let e, t = "No analysis data to display.";
  return {
    c() {
      e = T("p"), e.textContent = t, this.h();
    },
    l(s) {
      e = C(s, "P", { class: !0, "data-svelte-h": !0 }), K(e) !== "svelte-1q8w132" && (e.textContent = t), this.h();
    },
    h() {
      y(e, "class", "svelte-1stw26d");
    },
    m(s, i) {
      D(s, e, i);
    },
    p: Ae,
    d(s) {
      s && x(e);
    }
  };
}
function kn(n) {
  let e, t, s = "Original Code:", i, r, c, l = (
    /*display_value*/
    n[8].code + ""
  ), u, a, o, p, h = "Issue:", d, f, k = (
    /*display_value*/
    n[8].issue + ""
  ), g, I, E, B, R = "Reason:", q, $, z = (
    /*display_value*/
    n[8].reason + ""
  ), j, W, H, G, J, Ze = "Feedback", ye, Y, ie, ue = m.parse(
    /*display_value*/
    n[8].feedback || ""
  ) + "", A = (
    /*display_value*/
    n[8].fixed_code && st(n)
  );
  return {
    c() {
      e = T("div"), t = T("h4"), t.textContent = s, i = O(), r = T("pre"), c = T("code"), u = se(l), a = O(), o = T("div"), p = T("h4"), p.textContent = h, d = O(), f = T("p"), g = se(k), I = O(), E = T("div"), B = T("h4"), B.textContent = R, q = O(), $ = T("p"), j = se(z), W = O(), A && A.c(), H = O(), G = T("div"), J = T("h3"), J.textContent = Ze, ye = O(), Y = T("div"), ie = new cn(!1), this.h();
    },
    l(b) {
      e = C(b, "DIV", { class: !0 });
      var S = L(e);
      t = C(S, "H4", { class: !0, "data-svelte-h": !0 }), K(t) !== "svelte-1y38fdw" && (t.textContent = s), i = N(S), r = C(S, "PRE", { class: !0 });
      var Me = L(r);
      c = C(Me, "CODE", { class: !0 });
      var He = L(c);
      u = te(He, l), He.forEach(x), Me.forEach(x), S.forEach(x), a = N(b), o = C(b, "DIV", { class: !0 });
      var he = L(o);
      p = C(he, "H4", { class: !0, "data-svelte-h": !0 }), K(p) !== "svelte-1663oc9" && (p.textContent = h), d = N(he), f = C(he, "P", { class: !0 });
      var Ge = L(f);
      g = te(Ge, k), Ge.forEach(x), he.forEach(x), I = N(b), E = C(b, "DIV", { class: !0 });
      var pe = L(E);
      B = C(pe, "H4", { class: !0, "data-svelte-h": !0 }), K(B) !== "svelte-14axvnc" && (B.textContent = R), q = N(pe), $ = C(pe, "P", { class: !0 });
      var Fe = L($);
      j = te(Fe, z), Fe.forEach(x), pe.forEach(x), W = N(b), A && A.l(b), H = N(b), G = C(b, "DIV", { class: !0 });
      var fe = L(G);
      J = C(fe, "H3", { "data-svelte-h": !0 }), K(J) !== "svelte-76jzqn" && (J.textContent = Ze), ye = N(fe), Y = C(fe, "DIV", { class: !0 });
      var Qe = L(Y);
      ie = hn(Qe, !1), Qe.forEach(x), fe.forEach(x), this.h();
    },
    h() {
      y(t, "class", "svelte-1stw26d"), y(c, "class", "svelte-1stw26d"), y(r, "class", "svelte-1stw26d"), y(e, "class", "analysis-section svelte-1stw26d"), y(p, "class", "svelte-1stw26d"), y(f, "class", "svelte-1stw26d"), y(o, "class", "analysis-section svelte-1stw26d"), y(B, "class", "svelte-1stw26d"), y($, "class", "svelte-1stw26d"), y(E, "class", "analysis-section svelte-1stw26d"), ie.a = null, y(Y, "class", "markdown-content svelte-1stw26d"), y(G, "class", "feedback-section svelte-1stw26d");
    },
    m(b, S) {
      D(b, e, S), _(e, t), _(e, i), _(e, r), _(r, c), _(c, u), D(b, a, S), D(b, o, S), _(o, p), _(o, d), _(o, f), _(f, g), D(b, I, S), D(b, E, S), _(E, B), _(E, q), _(E, $), _($, j), D(b, W, S), A && A.m(b, S), D(b, H, S), D(b, G, S), _(G, J), _(G, ye), _(G, Y), ie.m(ue, Y);
    },
    p(b, S) {
      S & /*display_value*/
      256 && l !== (l = /*display_value*/
      b[8].code + "") && ne(u, l), S & /*display_value*/
      256 && k !== (k = /*display_value*/
      b[8].issue + "") && ne(g, k), S & /*display_value*/
      256 && z !== (z = /*display_value*/
      b[8].reason + "") && ne(j, z), /*display_value*/
      b[8].fixed_code ? A ? A.p(b, S) : (A = st(b), A.c(), A.m(H.parentNode, H)) : A && (A.d(1), A = null), S & /*display_value*/
      256 && ue !== (ue = m.parse(
        /*display_value*/
        b[8].feedback || ""
      ) + "") && ie.p(ue);
    },
    d(b) {
      b && (x(e), x(a), x(o), x(I), x(E), x(W), x(H), x(G)), A && A.d(b);
    }
  };
}
function st(n) {
  let e, t, s = "Suggested Fix (Diff):", i, r, c = Ke(
    /*codeDiff*/
    n[9]
  ), l = [];
  for (let u = 0; u < c.length; u += 1)
    l[u] = it(et(n, c, u));
  return {
    c() {
      e = T("div"), t = T("h4"), t.textContent = s, i = O(), r = T("pre");
      for (let u = 0; u < l.length; u += 1)
        l[u].c();
      this.h();
    },
    l(u) {
      e = C(u, "DIV", { class: !0 });
      var a = L(e);
      t = C(a, "H4", { class: !0, "data-svelte-h": !0 }), K(t) !== "svelte-18sigz6" && (t.textContent = s), i = N(a), r = C(a, "PRE", { class: !0 });
      var o = L(r);
      for (let p = 0; p < l.length; p += 1)
        l[p].l(o);
      o.forEach(x), a.forEach(x), this.h();
    },
    h() {
      y(t, "class", "svelte-1stw26d"), y(r, "class", "diff-view svelte-1stw26d"), y(e, "class", "analysis-section svelte-1stw26d");
    },
    m(u, a) {
      D(u, e, a), _(e, t), _(e, i), _(e, r);
      for (let o = 0; o < l.length; o += 1)
        l[o] && l[o].m(r, null);
    },
    p(u, a) {
      if (a & /*codeDiff*/
      512) {
        c = Ke(
          /*codeDiff*/
          u[9]
        );
        let o;
        for (o = 0; o < c.length; o += 1) {
          const p = et(u, c, o);
          l[o] ? l[o].p(p, a) : (l[o] = it(p), l[o].c(), l[o].m(r, null));
        }
        for (; o < l.length; o += 1)
          l[o].d(1);
        l.length = c.length;
      }
    },
    d(u) {
      u && x(e), pn(l, u);
    }
  };
}
function it(n) {
  let e, t = (
    /*part*/
    n[13].value + ""
  ), s, i;
  return {
    c() {
      e = T("span"), s = se(t), this.h();
    },
    l(r) {
      e = C(r, "SPAN", { class: !0 });
      var c = L(e);
      s = te(c, t), c.forEach(x), this.h();
    },
    h() {
      y(e, "class", i = "diff-part " + /*part*/
      (n[13].added ? "added" : (
        /*part*/
        n[13].removed ? "removed" : "common"
      )) + " svelte-1stw26d");
    },
    m(r, c) {
      D(r, e, c), _(e, s);
    },
    p(r, c) {
      c & /*codeDiff*/
      512 && t !== (t = /*part*/
      r[13].value + "") && ne(s, t), c & /*codeDiff*/
      512 && i !== (i = "diff-part " + /*part*/
      (r[13].added ? "added" : (
        /*part*/
        r[13].removed ? "removed" : "common"
      )) + " svelte-1stw26d") && y(e, "class", i);
    },
    d(r) {
      r && x(e);
    }
  };
}
function mn(n) {
  let e, t, s, i, r, c = (
    /*loading_status*/
    n[7] && tt(n)
  ), l = (
    /*show_label*/
    n[4] && nt(n)
  );
  function u(p, h) {
    return (
      /*display_value*/
      p[8] ? kn : gn
    );
  }
  let a = u(n), o = a(n);
  return {
    c() {
      e = T("div"), c && c.c(), t = O(), s = T("div"), l && l.c(), i = O(), o.c(), this.h();
    },
    l(p) {
      e = C(p, "DIV", { class: !0, id: !0, style: !0 });
      var h = L(e);
      c && c.l(h), t = N(h), s = C(h, "DIV", { class: !0 });
      var d = L(s);
      l && l.l(d), i = N(d), o.l(d), d.forEach(x), h.forEach(x), this.h();
    },
    h() {
      y(s, "class", "code-analysis-viewer svelte-1stw26d"), y(e, "class", "gradio-container"), y(e, "id", r = /*elem_id*/
      n[1] || null), ge(
        e,
        "width",
        /*scale*/
        n[5] || "auto"
      ), ge(
        e,
        "min-width",
        /*min_width*/
        n[6] + "px"
      ), ee(e, "hidden", !/*visible*/
      n[3]), ee(
        e,
        "block",
        /*elem_classes*/
        n[2].includes("block")
      );
    },
    m(p, h) {
      D(p, e, h), c && c.m(e, null), _(e, t), _(e, s), l && l.m(s, null), _(s, i), o.m(s, null);
    },
    p(p, [h]) {
      /*loading_status*/
      p[7] ? c ? c.p(p, h) : (c = tt(p), c.c(), c.m(e, t)) : c && (c.d(1), c = null), /*show_label*/
      p[4] ? l ? l.p(p, h) : (l = nt(p), l.c(), l.m(s, i)) : l && (l.d(1), l = null), a === (a = u(p)) && o ? o.p(p, h) : (o.d(1), o = a(p), o && (o.c(), o.m(s, null))), h & /*elem_id*/
      2 && r !== (r = /*elem_id*/
      p[1] || null) && y(e, "id", r), h & /*scale*/
      32 && ge(
        e,
        "width",
        /*scale*/
        p[5] || "auto"
      ), h & /*min_width*/
      64 && ge(
        e,
        "min-width",
        /*min_width*/
        p[6] + "px"
      ), h & /*visible*/
      8 && ee(e, "hidden", !/*visible*/
      p[3]), h & /*elem_classes*/
      4 && ee(
        e,
        "block",
        /*elem_classes*/
        p[2].includes("block")
      );
    },
    i: Ae,
    o: Ae,
    d(p) {
      p && x(e), c && c.d(), l && l.d(), o.d();
    }
  };
}
function bn(n, e, t) {
  let s;
  m.setOptions({
    breaks: !0,
    // Convert line breaks to <br>
    gfm: !0
    // Use GitHub Flavored Markdown
  });
  let { gradio: i } = e, { label: r = "Code Analysis" } = e, { elem_id: c = "" } = e, { elem_classes: l = [] } = e, { visible: u = !0 } = e, { value: a = null } = e, { show_label: o = !0 } = e, { scale: p = null } = e, { min_width: h = void 0 } = e, { loading_status: d = void 0 } = e;
  const f = {
    code: "// No code provided",
    issue: "No issues to display.",
    reason: "N/A",
    fixed_code: null,
    feedback: "No feedback available."
  };
  let k = [];
  return n.$$set = (g) => {
    "gradio" in g && t(10, i = g.gradio), "label" in g && t(0, r = g.label), "elem_id" in g && t(1, c = g.elem_id), "elem_classes" in g && t(2, l = g.elem_classes), "visible" in g && t(3, u = g.visible), "value" in g && t(11, a = g.value), "show_label" in g && t(4, o = g.show_label), "scale" in g && t(5, p = g.scale), "min_width" in g && t(6, h = g.min_width), "loading_status" in g && t(7, d = g.loading_status);
  }, n.$$.update = () => {
    n.$$.dirty & /*value, gradio*/
    3072 && a && i.dispatch("change", a), n.$$.dirty & /*value*/
    2048 && t(8, s = a || f), n.$$.dirty & /*display_value*/
    256 && (s && s.code && s.fixed_code ? t(9, k = _t(s.code, s.fixed_code)) : t(9, k = []));
  }, [
    r,
    c,
    l,
    u,
    o,
    p,
    h,
    d,
    s,
    k,
    i,
    a
  ];
}
class wn extends un {
  constructor(e) {
    super(), fn(this, e, bn, mn, dn, {
      gradio: 10,
      label: 0,
      elem_id: 1,
      elem_classes: 2,
      visible: 3,
      value: 11,
      show_label: 4,
      scale: 5,
      min_width: 6,
      loading_status: 7
    });
  }
  get gradio() {
    return this.$$.ctx[10];
  }
  set gradio(e) {
    this.$$set({ gradio: e }), Z();
  }
  get label() {
    return this.$$.ctx[0];
  }
  set label(e) {
    this.$$set({ label: e }), Z();
  }
  get elem_id() {
    return this.$$.ctx[1];
  }
  set elem_id(e) {
    this.$$set({ elem_id: e }), Z();
  }
  get elem_classes() {
    return this.$$.ctx[2];
  }
  set elem_classes(e) {
    this.$$set({ elem_classes: e }), Z();
  }
  get visible() {
    return this.$$.ctx[3];
  }
  set visible(e) {
    this.$$set({ visible: e }), Z();
  }
  get value() {
    return this.$$.ctx[11];
  }
  set value(e) {
    this.$$set({ value: e }), Z();
  }
  get show_label() {
    return this.$$.ctx[4];
  }
  set show_label(e) {
    this.$$set({ show_label: e }), Z();
  }
  get scale() {
    return this.$$.ctx[5];
  }
  set scale(e) {
    this.$$set({ scale: e }), Z();
  }
  get min_width() {
    return this.$$.ctx[6];
  }
  set min_width(e) {
    this.$$set({ min_width: e }), Z();
  }
  get loading_status() {
    return this.$$.ctx[7];
  }
  set loading_status(e) {
    this.$$set({ loading_status: e }), Z();
  }
}
export {
  wn as default
};
