var hl = Object.defineProperty;
var wa = (e) => {
  throw TypeError(e);
};
var bl = (e, t, n) => t in e ? hl(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var ya = (e, t, n) => bl(e, typeof t != "symbol" ? t + "" : t, n), Sr = (e, t, n) => t.has(e) || wa("Cannot " + n);
var oe = (e, t, n) => (Sr(e, t, "read from private field"), n ? n.call(e) : t.get(e)), Fe = (e, t, n) => t.has(e) ? wa("Cannot add the same private member more than once") : t instanceof WeakSet ? t.add(e) : t.set(e, n), We = (e, t, n, r) => (Sr(e, t, "write to private field"), r ? r.call(e, n) : t.set(e, n), n), ka = (e, t, n) => (Sr(e, t, "access private method"), n);
const _l = "5";
var vi;
typeof window < "u" && ((vi = window.__svelte ?? (window.__svelte = {})).v ?? (vi.v = /* @__PURE__ */ new Set())).add(_l);
const Jr = 1, $r = 2, gi = 4, ml = 8, xl = 16, pl = 1, wl = 4, yl = 8, kl = 16, hi = 1, Ml = 2, Ie = Symbol(), Tl = "http://www.w3.org/1999/xhtml", Ma = !1;
var or = Array.isArray, Al = Array.prototype.indexOf, ea = Array.from, Sl = Object.defineProperty, yt = Object.getOwnPropertyDescriptor, El = Object.getOwnPropertyDescriptors, Ll = Object.prototype, Nl = Array.prototype, bi = Object.getPrototypeOf, Ta = Object.isExtensible;
function ln(e) {
  return typeof e == "function";
}
const Fl = () => {
};
function Cl(e) {
  for (var t = 0; t < e.length; t++)
    e[t]();
}
const tt = 2, _i = 4, fr = 8, ta = 16, bt = 32, $t = 64, Hn = 128, Xe = 256, jn = 512, He = 1024, ot = 2048, Pt = 4096, vt = 8192, ur = 16384, ql = 32768, cr = 65536, Pl = 1 << 19, mi = 1 << 20, zr = 1 << 21, kt = Symbol("$state"), xi = Symbol("legacy props"), Rl = Symbol("");
function pi(e) {
  return e === this.v;
}
function zl(e, t) {
  return e != e ? t == t : e !== t || e !== null && typeof e == "object" || typeof e == "function";
}
function na(e) {
  return !zl(e, this.v);
}
function Il(e) {
  throw new Error("https://svelte.dev/e/effect_in_teardown");
}
function Dl() {
  throw new Error("https://svelte.dev/e/effect_in_unowned_derived");
}
function Ol(e) {
  throw new Error("https://svelte.dev/e/effect_orphan");
}
function Bl() {
  throw new Error("https://svelte.dev/e/effect_update_depth_exceeded");
}
function Hl(e) {
  throw new Error("https://svelte.dev/e/props_invalid_value");
}
function jl() {
  throw new Error("https://svelte.dev/e/state_descriptors_fixed");
}
function Wl() {
  throw new Error("https://svelte.dev/e/state_prototype_fixed");
}
function Vl() {
  throw new Error("https://svelte.dev/e/state_unsafe_mutation");
}
let Yl = !1, Ge = null;
function Aa(e) {
  Ge = e;
}
function me(e, t = !1, n) {
  var r = Ge = {
    p: Ge,
    c: null,
    d: !1,
    e: null,
    m: !1,
    s: e,
    x: null,
    l: null
  };
  Ni(() => {
    r.d = !0;
  });
}
function xe(e) {
  const t = Ge;
  if (t !== null) {
    const s = t.e;
    if (s !== null) {
      var n = be, r = ge;
      t.e = null;
      try {
        for (var a = 0; a < s.length; a++) {
          var i = s[a];
          Mt(i.effect), ft(i.reaction), tn(i.fn);
        }
      } finally {
        Mt(n), ft(r);
      }
    }
    Ge = t.p, t.m = !0;
  }
  return (
    /** @type {T} */
    {}
  );
}
function wi() {
  return !0;
}
function at(e) {
  if (typeof e != "object" || e === null || kt in e)
    return e;
  const t = bi(e);
  if (t !== Ll && t !== Nl)
    return e;
  var n = /* @__PURE__ */ new Map(), r = or(e), a = /* @__PURE__ */ se(0), i = ge, s = (o) => {
    var u = ge;
    ft(i);
    var f = o();
    return ft(u), f;
  };
  return r && n.set("length", /* @__PURE__ */ se(
    /** @type {any[]} */
    e.length
  )), new Proxy(
    /** @type {any} */
    e,
    {
      defineProperty(o, u, f) {
        (!("value" in f) || f.configurable === !1 || f.enumerable === !1 || f.writable === !1) && jl();
        var v = n.get(u);
        return v === void 0 ? (v = s(() => /* @__PURE__ */ se(f.value)), n.set(u, v)) : ee(
          v,
          s(() => at(f.value))
        ), !0;
      },
      deleteProperty(o, u) {
        var f = n.get(u);
        if (f === void 0)
          u in o && (n.set(
            u,
            s(() => /* @__PURE__ */ se(Ie))
          ), Er(a));
        else {
          if (r && typeof u == "string") {
            var v = (
              /** @type {Source<number>} */
              n.get("length")
            ), c = Number(u);
            Number.isInteger(c) && c < v.v && ee(v, c);
          }
          ee(f, Ie), Er(a);
        }
        return !0;
      },
      get(o, u, f) {
        var g;
        if (u === kt)
          return e;
        var v = n.get(u), c = u in o;
        if (v === void 0 && (!c || (g = yt(o, u)) != null && g.writable) && (v = s(() => /* @__PURE__ */ se(at(c ? o[u] : Ie))), n.set(u, v)), v !== void 0) {
          var d = l(v);
          return d === Ie ? void 0 : d;
        }
        return Reflect.get(o, u, f);
      },
      getOwnPropertyDescriptor(o, u) {
        var f = Reflect.getOwnPropertyDescriptor(o, u);
        if (f && "value" in f) {
          var v = n.get(u);
          v && (f.value = l(v));
        } else if (f === void 0) {
          var c = n.get(u), d = c == null ? void 0 : c.v;
          if (c !== void 0 && d !== Ie)
            return {
              enumerable: !0,
              configurable: !0,
              value: d,
              writable: !0
            };
        }
        return f;
      },
      has(o, u) {
        var d;
        if (u === kt)
          return !0;
        var f = n.get(u), v = f !== void 0 && f.v !== Ie || Reflect.has(o, u);
        if (f !== void 0 || be !== null && (!v || (d = yt(o, u)) != null && d.writable)) {
          f === void 0 && (f = s(() => /* @__PURE__ */ se(v ? at(o[u]) : Ie)), n.set(u, f));
          var c = l(f);
          if (c === Ie)
            return !1;
        }
        return v;
      },
      set(o, u, f, v) {
        var k;
        var c = n.get(u), d = u in o;
        if (r && u === "length")
          for (var g = f; g < /** @type {Source<number>} */
          c.v; g += 1) {
            var h = n.get(g + "");
            h !== void 0 ? ee(h, Ie) : g in o && (h = s(() => /* @__PURE__ */ se(Ie)), n.set(g + "", h));
          }
        c === void 0 ? (!d || (k = yt(o, u)) != null && k.writable) && (c = s(() => /* @__PURE__ */ se(void 0)), ee(
          c,
          s(() => at(f))
        ), n.set(u, c)) : (d = c.v !== Ie, ee(
          c,
          s(() => at(f))
        ));
        var _ = Reflect.getOwnPropertyDescriptor(o, u);
        if (_ != null && _.set && _.set.call(v, f), !d) {
          if (r && typeof u == "string") {
            var w = (
              /** @type {Source<number>} */
              n.get("length")
            ), T = Number(u);
            Number.isInteger(T) && T >= w.v && ee(w, T + 1);
          }
          Er(a);
        }
        return !0;
      },
      ownKeys(o) {
        l(a);
        var u = Reflect.ownKeys(o).filter((c) => {
          var d = n.get(c);
          return d === void 0 || d.v !== Ie;
        });
        for (var [f, v] of n)
          v.v !== Ie && !(f in o) && u.push(f);
        return u;
      },
      setPrototypeOf() {
        Wl();
      }
    }
  );
}
function Er(e, t = 1) {
  ee(e, e.v + t);
}
function Sa(e) {
  try {
    if (e !== null && typeof e == "object" && kt in e)
      return e[kt];
  } catch {
  }
  return e;
}
function Xl(e, t) {
  return Object.is(Sa(e), Sa(t));
}
// @__NO_SIDE_EFFECTS__
function dr(e) {
  var t = tt | ot, n = ge !== null && (ge.f & tt) !== 0 ? (
    /** @type {Derived} */
    ge
  ) : null;
  return be === null || n !== null && (n.f & Xe) !== 0 ? t |= Xe : be.f |= mi, {
    ctx: Ge,
    deps: null,
    effects: null,
    equals: pi,
    f: t,
    fn: e,
    reactions: null,
    rv: 0,
    v: (
      /** @type {V} */
      null
    ),
    wv: 0,
    parent: n ?? be
  };
}
// @__NO_SIDE_EFFECTS__
function x(e) {
  const t = /* @__PURE__ */ dr(e);
  return zi(t), t;
}
// @__NO_SIDE_EFFECTS__
function Gl(e) {
  const t = /* @__PURE__ */ dr(e);
  return t.equals = na, t;
}
function yi(e) {
  var t = e.effects;
  if (t !== null) {
    e.effects = null;
    for (var n = 0; n < t.length; n += 1)
      ht(
        /** @type {Effect} */
        t[n]
      );
  }
}
function Ul(e) {
  for (var t = e.parent; t !== null; ) {
    if ((t.f & tt) === 0)
      return (
        /** @type {Effect} */
        t
      );
    t = t.parent;
  }
  return null;
}
function ki(e) {
  var t, n = be;
  Mt(Ul(e));
  try {
    yi(e), t = Bi(e);
  } finally {
    Mt(n);
  }
  return t;
}
function Mi(e) {
  var t = ki(e);
  if (e.equals(t) || (e.v = t, e.wv = Di()), !nn) {
    var n = (wt || (e.f & Xe) !== 0) && e.deps !== null ? Pt : He;
    nt(e, n);
  }
}
const dn = /* @__PURE__ */ new Map();
function Wn(e, t) {
  var n = {
    f: 0,
    // TODO ideally we could skip this altogether, but it causes type errors
    v: e,
    reactions: null,
    equals: pi,
    rv: 0,
    wv: 0
  };
  return n;
}
// @__NO_SIDE_EFFECTS__
function se(e, t) {
  const n = Wn(e);
  return zi(n), n;
}
// @__NO_SIDE_EFFECTS__
function Ti(e, t = !1) {
  const n = Wn(e);
  return t || (n.equals = na), n;
}
function ee(e, t, n = !1) {
  ge !== null && !it && wi() && (ge.f & (tt | ta)) !== 0 && !(Pe != null && Pe.includes(e)) && Vl();
  let r = n ? at(t) : t;
  return Ir(e, r);
}
function Ir(e, t) {
  if (!e.equals(t)) {
    var n = e.v;
    nn ? dn.set(e, t) : dn.set(e, n), e.v = t, (e.f & tt) !== 0 && ((e.f & ot) !== 0 && ki(
      /** @type {Derived} */
      e
    ), nt(e, (e.f & Xe) === 0 ? He : Pt)), e.wv = Di(), Ai(e, ot), be !== null && (be.f & He) !== 0 && (be.f & (bt | $t)) === 0 && (Ke === null ? is([e]) : Ke.push(e));
  }
  return t;
}
function Ai(e, t) {
  var n = e.reactions;
  if (n !== null)
    for (var r = n.length, a = 0; a < r; a++) {
      var i = n[a], s = i.f;
      (s & ot) === 0 && (nt(i, t), (s & (He | Xe)) !== 0 && ((s & tt) !== 0 ? Ai(
        /** @type {Derived} */
        i,
        Pt
      ) : _r(
        /** @type {Effect} */
        i
      )));
    }
}
function Kl() {
  console.warn("https://svelte.dev/e/select_multiple_invalid_value");
}
let Zl = !1;
var Ea, Si, Ei, Li;
function Ql() {
  if (Ea === void 0) {
    Ea = window, Si = /Firefox/.test(navigator.userAgent);
    var e = Element.prototype, t = Node.prototype, n = Text.prototype;
    Ei = yt(t, "firstChild").get, Li = yt(t, "nextSibling").get, Ta(e) && (e.__click = void 0, e.__className = void 0, e.__attributes = null, e.__style = void 0, e.__e = void 0), Ta(n) && (n.__t = void 0);
  }
}
function vr(e = "") {
  return document.createTextNode(e);
}
// @__NO_SIDE_EFFECTS__
function dt(e) {
  return Ei.call(e);
}
// @__NO_SIDE_EFFECTS__
function gr(e) {
  return Li.call(e);
}
function b(e, t) {
  return /* @__PURE__ */ dt(e);
}
function Ee(e, t) {
  {
    var n = (
      /** @type {DocumentFragment} */
      /* @__PURE__ */ dt(
        /** @type {Node} */
        e
      )
    );
    return n instanceof Comment && n.data === "" ? /* @__PURE__ */ gr(n) : n;
  }
}
function m(e, t = 1, n = !1) {
  let r = e;
  for (; t--; )
    r = /** @type {TemplateNode} */
    /* @__PURE__ */ gr(r);
  return r;
}
function Jl(e) {
  e.textContent = "";
}
function $l(e) {
  be === null && ge === null && Ol(), ge !== null && (ge.f & Xe) !== 0 && be === null && Dl(), nn && Il();
}
function es(e, t) {
  var n = t.last;
  n === null ? t.last = t.first = e : (n.next = e, e.prev = n, t.last = e);
}
function en(e, t, n, r = !0) {
  var a = be, i = {
    ctx: Ge,
    deps: null,
    nodes_start: null,
    nodes_end: null,
    f: e | ot,
    first: null,
    fn: t,
    last: null,
    next: null,
    parent: a,
    prev: null,
    teardown: null,
    transitions: null,
    wv: 0
  };
  if (n)
    try {
      la(i), i.f |= ql;
    } catch (u) {
      throw ht(i), u;
    }
  else t !== null && _r(i);
  var s = n && i.deps === null && i.first === null && i.nodes_start === null && i.teardown === null && (i.f & (mi | Hn)) === 0;
  if (!s && r && (a !== null && es(i, a), ge !== null && (ge.f & tt) !== 0)) {
    var o = (
      /** @type {Derived} */
      ge
    );
    (o.effects ?? (o.effects = [])).push(i);
  }
  return i;
}
function Ni(e) {
  const t = en(fr, null, !1);
  return nt(t, He), t.teardown = e, t;
}
function Dr(e) {
  $l();
  var t = be !== null && (be.f & bt) !== 0 && Ge !== null && !Ge.m;
  if (t) {
    var n = (
      /** @type {ComponentContext} */
      Ge
    );
    (n.e ?? (n.e = [])).push({
      fn: e,
      effect: be,
      reaction: ge
    });
  } else {
    var r = tn(e);
    return r;
  }
}
function ts(e) {
  const t = en($t, e, !0);
  return (n = {}) => new Promise((r) => {
    n.outro ? Vn(t, () => {
      ht(t), r(void 0);
    }) : (ht(t), r(void 0));
  });
}
function tn(e) {
  return en(_i, e, !1);
}
function ra(e) {
  return en(fr, e, !0);
}
function ne(e, t = [], n = dr) {
  const r = t.map(n);
  return hr(() => e(...r.map(l)));
}
function hr(e, t = 0) {
  return en(fr | ta | t, e, !0);
}
function Gt(e, t = !0) {
  return en(fr | bt, e, !0, t);
}
function Fi(e) {
  var t = e.teardown;
  if (t !== null) {
    const n = nn, r = ge;
    La(!0), ft(null);
    try {
      t.call(null);
    } finally {
      La(n), ft(r);
    }
  }
}
function Ci(e, t = !1) {
  var n = e.first;
  for (e.first = e.last = null; n !== null; ) {
    var r = n.next;
    (n.f & $t) !== 0 ? n.parent = null : ht(n, t), n = r;
  }
}
function ns(e) {
  for (var t = e.first; t !== null; ) {
    var n = t.next;
    (t.f & bt) === 0 && ht(t), t = n;
  }
}
function ht(e, t = !0) {
  var n = !1;
  (t || (e.f & Pl) !== 0) && e.nodes_start !== null && (rs(
    e.nodes_start,
    /** @type {TemplateNode} */
    e.nodes_end
  ), n = !0), Ci(e, t && !n), Kn(e, 0), nt(e, ur);
  var r = e.transitions;
  if (r !== null)
    for (const i of r)
      i.stop();
  Fi(e);
  var a = e.parent;
  a !== null && a.first !== null && qi(e), e.next = e.prev = e.teardown = e.ctx = e.deps = e.fn = e.nodes_start = e.nodes_end = null;
}
function rs(e, t) {
  for (; e !== null; ) {
    var n = e === t ? null : (
      /** @type {TemplateNode} */
      /* @__PURE__ */ gr(e)
    );
    e.remove(), e = n;
  }
}
function qi(e) {
  var t = e.parent, n = e.prev, r = e.next;
  n !== null && (n.next = r), r !== null && (r.prev = n), t !== null && (t.first === e && (t.first = r), t.last === e && (t.last = n));
}
function Vn(e, t) {
  var n = [];
  aa(e, n, !0), Pi(n, () => {
    ht(e), t && t();
  });
}
function Pi(e, t) {
  var n = e.length;
  if (n > 0) {
    var r = () => --n || t();
    for (var a of e)
      a.out(r);
  } else
    t();
}
function aa(e, t, n) {
  if ((e.f & vt) === 0) {
    if (e.f ^= vt, e.transitions !== null)
      for (const s of e.transitions)
        (s.is_global || n) && t.push(s);
    for (var r = e.first; r !== null; ) {
      var a = r.next, i = (r.f & cr) !== 0 || (r.f & bt) !== 0;
      aa(r, t, i ? n : !1), r = a;
    }
  }
}
function Yn(e) {
  Ri(e, !0);
}
function Ri(e, t) {
  if ((e.f & vt) !== 0) {
    e.f ^= vt, (e.f & He) === 0 && (e.f ^= He), kn(e) && (nt(e, ot), _r(e));
    for (var n = e.first; n !== null; ) {
      var r = n.next, a = (n.f & cr) !== 0 || (n.f & bt) !== 0;
      Ri(n, a ? t : !1), n = r;
    }
    if (e.transitions !== null)
      for (const i of e.transitions)
        (i.is_global || t) && i.in();
  }
}
let Xn = [];
function as() {
  var e = Xn;
  Xn = [], Cl(e);
}
function ia(e) {
  Xn.length === 0 && queueMicrotask(as), Xn.push(e);
}
let Nn = !1, Or = !1, Gn = null, Lt = !1, nn = !1;
function La(e) {
  nn = e;
}
let Fn = [];
let ge = null, it = !1;
function ft(e) {
  ge = e;
}
let be = null;
function Mt(e) {
  be = e;
}
let Pe = null;
function zi(e) {
  ge !== null && ge.f & zr && (Pe === null ? Pe = [e] : Pe.push(e));
}
let Ce = null, Ve = 0, Ke = null;
function is(e) {
  Ke = e;
}
let Ii = 1, Un = 0, wt = !1;
function Di() {
  return ++Ii;
}
function kn(e) {
  var c;
  var t = e.f;
  if ((t & ot) !== 0)
    return !0;
  if ((t & Pt) !== 0) {
    var n = e.deps, r = (t & Xe) !== 0;
    if (n !== null) {
      var a, i, s = (t & jn) !== 0, o = r && be !== null && !wt, u = n.length;
      if (s || o) {
        var f = (
          /** @type {Derived} */
          e
        ), v = f.parent;
        for (a = 0; a < u; a++)
          i = n[a], (s || !((c = i == null ? void 0 : i.reactions) != null && c.includes(f))) && (i.reactions ?? (i.reactions = [])).push(f);
        s && (f.f ^= jn), o && v !== null && (v.f & Xe) === 0 && (f.f ^= Xe);
      }
      for (a = 0; a < u; a++)
        if (i = n[a], kn(
          /** @type {Derived} */
          i
        ) && Mi(
          /** @type {Derived} */
          i
        ), i.wv > e.wv)
          return !0;
    }
    (!r || be !== null && !wt) && nt(e, He);
  }
  return !1;
}
function ls(e, t) {
  for (var n = t; n !== null; ) {
    if ((n.f & Hn) !== 0)
      try {
        n.fn(e);
        return;
      } catch {
        n.f ^= Hn;
      }
    n = n.parent;
  }
  throw Nn = !1, e;
}
function Na(e) {
  return (e.f & ur) === 0 && (e.parent === null || (e.parent.f & Hn) === 0);
}
function br(e, t, n, r) {
  if (Nn) {
    if (n === null && (Nn = !1), Na(t))
      throw e;
    return;
  }
  if (n !== null && (Nn = !0), ls(e, t), Na(t))
    throw e;
}
function Oi(e, t, n = !0) {
  var r = e.reactions;
  if (r !== null)
    for (var a = 0; a < r.length; a++) {
      var i = r[a];
      Pe != null && Pe.includes(e) || ((i.f & tt) !== 0 ? Oi(
        /** @type {Derived} */
        i,
        t,
        !1
      ) : t === i && (n ? nt(i, ot) : (i.f & He) !== 0 && nt(i, Pt), _r(
        /** @type {Effect} */
        i
      )));
    }
}
function Bi(e) {
  var g;
  var t = Ce, n = Ve, r = Ke, a = ge, i = wt, s = Pe, o = Ge, u = it, f = e.f;
  Ce = /** @type {null | Value[]} */
  null, Ve = 0, Ke = null, wt = (f & Xe) !== 0 && (it || !Lt || ge === null), ge = (f & (bt | $t)) === 0 ? e : null, Pe = null, Aa(e.ctx), it = !1, Un++, e.f |= zr;
  try {
    var v = (
      /** @type {Function} */
      (0, e.fn)()
    ), c = e.deps;
    if (Ce !== null) {
      var d;
      if (Kn(e, Ve), c !== null && Ve > 0)
        for (c.length = Ve + Ce.length, d = 0; d < Ce.length; d++)
          c[Ve + d] = Ce[d];
      else
        e.deps = c = Ce;
      if (!wt)
        for (d = Ve; d < c.length; d++)
          ((g = c[d]).reactions ?? (g.reactions = [])).push(e);
    } else c !== null && Ve < c.length && (Kn(e, Ve), c.length = Ve);
    if (wi() && Ke !== null && !it && c !== null && (e.f & (tt | Pt | ot)) === 0)
      for (d = 0; d < /** @type {Source[]} */
      Ke.length; d++)
        Oi(
          Ke[d],
          /** @type {Effect} */
          e
        );
    return a !== null && a !== e && (Un++, Ke !== null && (r === null ? r = Ke : r.push(.../** @type {Source[]} */
    Ke))), v;
  } finally {
    Ce = t, Ve = n, Ke = r, ge = a, wt = i, Pe = s, Aa(o), it = u, e.f ^= zr;
  }
}
function ss(e, t) {
  let n = t.reactions;
  if (n !== null) {
    var r = Al.call(n, e);
    if (r !== -1) {
      var a = n.length - 1;
      a === 0 ? n = t.reactions = null : (n[r] = n[a], n.pop());
    }
  }
  n === null && (t.f & tt) !== 0 && // Destroying a child effect while updating a parent effect can cause a dependency to appear
  // to be unused, when in fact it is used by the currently-updating parent. Checking `new_deps`
  // allows us to skip the expensive work of disconnecting and immediately reconnecting it
  (Ce === null || !Ce.includes(t)) && (nt(t, Pt), (t.f & (Xe | jn)) === 0 && (t.f ^= jn), yi(
    /** @type {Derived} **/
    t
  ), Kn(
    /** @type {Derived} **/
    t,
    0
  ));
}
function Kn(e, t) {
  var n = e.deps;
  if (n !== null)
    for (var r = t; r < n.length; r++)
      ss(e, n[r]);
}
function la(e) {
  var t = e.f;
  if ((t & ur) === 0) {
    nt(e, He);
    var n = be, r = Ge, a = Lt;
    be = e, Lt = !0;
    try {
      (t & ta) !== 0 ? ns(e) : Ci(e), Fi(e);
      var i = Bi(e);
      e.teardown = typeof i == "function" ? i : null, e.wv = Ii;
      var s = e.deps, o;
      Ma && Yl && e.f & ot;
    } catch (u) {
      br(u, e, n, r || e.ctx);
    } finally {
      Lt = a, be = n;
    }
  }
}
function os() {
  try {
    Bl();
  } catch (e) {
    if (Gn !== null)
      br(e, Gn, null);
    else
      throw e;
  }
}
function fs() {
  var e = Lt;
  try {
    var t = 0;
    for (Lt = !0; Fn.length > 0; ) {
      t++ > 1e3 && os();
      var n = Fn, r = n.length;
      Fn = [];
      for (var a = 0; a < r; a++) {
        var i = cs(n[a]);
        us(i);
      }
      dn.clear();
    }
  } finally {
    Or = !1, Lt = e, Gn = null;
  }
}
function us(e) {
  var t = e.length;
  if (t !== 0)
    for (var n = 0; n < t; n++) {
      var r = e[n];
      if ((r.f & (ur | vt)) === 0)
        try {
          kn(r) && (la(r), r.deps === null && r.first === null && r.nodes_start === null && (r.teardown === null ? qi(r) : r.fn = null));
        } catch (a) {
          br(a, r, null, r.ctx);
        }
    }
}
function _r(e) {
  Or || (Or = !0, queueMicrotask(fs));
  for (var t = Gn = e; t.parent !== null; ) {
    t = t.parent;
    var n = t.f;
    if ((n & ($t | bt)) !== 0) {
      if ((n & He) === 0) return;
      t.f ^= He;
    }
  }
  Fn.push(t);
}
function cs(e) {
  for (var t = [], n = e; n !== null; ) {
    var r = n.f, a = (r & (bt | $t)) !== 0, i = a && (r & He) !== 0;
    if (!i && (r & vt) === 0) {
      if ((r & _i) !== 0)
        t.push(n);
      else if (a)
        n.f ^= He;
      else
        try {
          kn(n) && la(n);
        } catch (u) {
          br(u, n, null, n.ctx);
        }
      var s = n.first;
      if (s !== null) {
        n = s;
        continue;
      }
    }
    var o = n.parent;
    for (n = n.next; n === null && o !== null; )
      n = o.next, o = o.parent;
  }
  return t;
}
function l(e) {
  var t = e.f, n = (t & tt) !== 0;
  if (ge !== null && !it) {
    if (!(Pe != null && Pe.includes(e))) {
      var r = ge.deps;
      e.rv < Un && (e.rv = Un, Ce === null && r !== null && r[Ve] === e ? Ve++ : Ce === null ? Ce = [e] : (!wt || !Ce.includes(e)) && Ce.push(e));
    }
  } else if (n && /** @type {Derived} */
  e.deps === null && /** @type {Derived} */
  e.effects === null) {
    var a = (
      /** @type {Derived} */
      e
    ), i = a.parent;
    i !== null && (i.f & Xe) === 0 && (a.f ^= Xe);
  }
  return n && (a = /** @type {Derived} */
  e, kn(a) && Mi(a)), nn && dn.has(e) ? dn.get(e) : e.v;
}
function Ct(e) {
  var t = it;
  try {
    return it = !0, e();
  } finally {
    it = t;
  }
}
const ds = -7169;
function nt(e, t) {
  e.f = e.f & ds | t;
}
let Fa = !1;
function vs() {
  Fa || (Fa = !0, document.addEventListener(
    "reset",
    (e) => {
      Promise.resolve().then(() => {
        var t;
        if (!e.defaultPrevented)
          for (
            const n of
            /**@type {HTMLFormElement} */
            e.target.elements
          )
            (t = n.__on_r) == null || t.call(n);
      });
    },
    // In the capture phase to guarantee we get noticed of it (no possiblity of stopPropagation)
    { capture: !0 }
  ));
}
function Hi(e) {
  var t = ge, n = be;
  ft(null), Mt(null);
  try {
    return e();
  } finally {
    ft(t), Mt(n);
  }
}
function sa(e, t, n, r = n) {
  e.addEventListener(t, () => Hi(n));
  const a = e.__on_r;
  a ? e.__on_r = () => {
    a(), r(!0);
  } : e.__on_r = () => r(!0), vs();
}
const ji = /* @__PURE__ */ new Set(), Br = /* @__PURE__ */ new Set();
function gs(e, t, n, r = {}) {
  function a(i) {
    if (r.capture || on.call(t, i), !i.cancelBubble)
      return Hi(() => n == null ? void 0 : n.call(this, i));
  }
  return e.startsWith("pointer") || e.startsWith("touch") || e === "wheel" ? ia(() => {
    t.addEventListener(e, a, r);
  }) : t.addEventListener(e, a, r), a;
}
function Je(e, t, n, r, a) {
  var i = { capture: r, passive: a }, s = gs(e, t, n, i);
  (t === document.body || // @ts-ignore
  t === window || // @ts-ignore
  t === document || // Firefox has quirky behavior, it can happen that we still get "canplay" events when the element is already removed
  t instanceof HTMLMediaElement) && Ni(() => {
    t.removeEventListener(e, s, i);
  });
}
function Rt(e) {
  for (var t = 0; t < e.length; t++)
    ji.add(e[t]);
  for (var n of Br)
    n(e);
}
function on(e) {
  var k;
  var t = this, n = (
    /** @type {Node} */
    t.ownerDocument
  ), r = e.type, a = ((k = e.composedPath) == null ? void 0 : k.call(e)) || [], i = (
    /** @type {null | Element} */
    a[0] || e.target
  ), s = 0, o = e.__root;
  if (o) {
    var u = a.indexOf(o);
    if (u !== -1 && (t === document || t === /** @type {any} */
    window)) {
      e.__root = t;
      return;
    }
    var f = a.indexOf(t);
    if (f === -1)
      return;
    u <= f && (s = u);
  }
  if (i = /** @type {Element} */
  a[s] || e.target, i !== t) {
    Sl(e, "currentTarget", {
      configurable: !0,
      get() {
        return i || n;
      }
    });
    var v = ge, c = be;
    ft(null), Mt(null);
    try {
      for (var d, g = []; i !== null; ) {
        var h = i.assignedSlot || i.parentNode || /** @type {any} */
        i.host || null;
        try {
          var _ = i["__" + r];
          if (_ != null && (!/** @type {any} */
          i.disabled || // DOM could've been updated already by the time this is reached, so we check this as well
          // -> the target could not have been disabled because it emits the event in the first place
          e.target === i))
            if (or(_)) {
              var [w, ...T] = _;
              w.apply(i, [e, ...T]);
            } else
              _.call(i, e);
        } catch (p) {
          d ? g.push(p) : d = p;
        }
        if (e.cancelBubble || h === t || h === null)
          break;
        i = h;
      }
      if (d) {
        for (let p of g)
          queueMicrotask(() => {
            throw p;
          });
        throw d;
      }
    } finally {
      e.__root = t, delete e.currentTarget, ft(v), Mt(c);
    }
  }
}
function Wi(e) {
  var t = document.createElement("template");
  return t.innerHTML = e.replaceAll("<!>", "<!---->"), t.content;
}
function Ut(e, t) {
  var n = (
    /** @type {Effect} */
    be
  );
  n.nodes_start === null && (n.nodes_start = e, n.nodes_end = t);
}
// @__NO_SIDE_EFFECTS__
function te(e, t) {
  var n = (t & hi) !== 0, r = (t & Ml) !== 0, a, i = !e.startsWith("<!>");
  return () => {
    a === void 0 && (a = Wi(i ? e : "<!>" + e), n || (a = /** @type {Node} */
    /* @__PURE__ */ dt(a)));
    var s = (
      /** @type {TemplateNode} */
      r || Si ? document.importNode(a, !0) : a.cloneNode(!0)
    );
    if (n) {
      var o = (
        /** @type {TemplateNode} */
        /* @__PURE__ */ dt(s)
      ), u = (
        /** @type {TemplateNode} */
        s.lastChild
      );
      Ut(o, u);
    } else
      Ut(s, s);
    return s;
  };
}
// @__NO_SIDE_EFFECTS__
function hs(e, t, n = "svg") {
  var r = !e.startsWith("<!>"), a = (t & hi) !== 0, i = `<${n}>${r ? e : "<!>" + e}</${n}>`, s;
  return () => {
    if (!s) {
      var o = (
        /** @type {DocumentFragment} */
        Wi(i)
      ), u = (
        /** @type {Element} */
        /* @__PURE__ */ dt(o)
      );
      if (a)
        for (s = document.createDocumentFragment(); /* @__PURE__ */ dt(u); )
          s.appendChild(
            /** @type {Node} */
            /* @__PURE__ */ dt(u)
          );
      else
        s = /** @type {Element} */
        /* @__PURE__ */ dt(u);
    }
    var f = (
      /** @type {TemplateNode} */
      s.cloneNode(!0)
    );
    if (a) {
      var v = (
        /** @type {TemplateNode} */
        /* @__PURE__ */ dt(f)
      ), c = (
        /** @type {TemplateNode} */
        f.lastChild
      );
      Ut(v, c);
    } else
      Ut(f, f);
    return f;
  };
}
// @__NO_SIDE_EFFECTS__
function we(e, t) {
  return /* @__PURE__ */ hs(e, t, "svg");
}
function Ca(e = "") {
  {
    var t = vr(e + "");
    return Ut(t, t), t;
  }
}
function qt() {
  var e = document.createDocumentFragment(), t = document.createComment(""), n = vr();
  return e.append(t, n), Ut(t, n), e;
}
function I(e, t) {
  e !== null && e.before(
    /** @type {Node} */
    t
  );
}
function bs() {
  var e;
  return (e = window.__svelte ?? (window.__svelte = {})).uid ?? (e.uid = 1), `c${window.__svelte.uid++}`;
}
const _s = ["touchstart", "touchmove"];
function ms(e) {
  return _s.includes(e);
}
function de(e, t) {
  var n = t == null ? "" : typeof t == "object" ? t + "" : t;
  n !== (e.__t ?? (e.__t = e.nodeValue)) && (e.__t = n, e.nodeValue = n + "");
}
function xs(e, t) {
  return ps(e, t);
}
const zt = /* @__PURE__ */ new Map();
function ps(e, { target: t, anchor: n, props: r = {}, events: a, context: i, intro: s = !0 }) {
  Ql();
  var o = /* @__PURE__ */ new Set(), u = (c) => {
    for (var d = 0; d < c.length; d++) {
      var g = c[d];
      if (!o.has(g)) {
        o.add(g);
        var h = ms(g);
        t.addEventListener(g, on, { passive: h });
        var _ = zt.get(g);
        _ === void 0 ? (document.addEventListener(g, on, { passive: h }), zt.set(g, 1)) : zt.set(g, _ + 1);
      }
    }
  };
  u(ea(ji)), Br.add(u);
  var f = void 0, v = ts(() => {
    var c = n ?? t.appendChild(vr());
    return Gt(() => {
      if (i) {
        me({});
        var d = (
          /** @type {ComponentContext} */
          Ge
        );
        d.c = i;
      }
      a && (r.$$events = a), f = e(c, r) || {}, i && xe();
    }), () => {
      var h;
      for (var d of o) {
        t.removeEventListener(d, on);
        var g = (
          /** @type {number} */
          zt.get(d)
        );
        --g === 0 ? (document.removeEventListener(d, on), zt.delete(d)) : zt.set(d, g);
      }
      Br.delete(u), c !== n && ((h = c.parentNode) == null || h.removeChild(c));
    };
  });
  return Hr.set(f, v), f;
}
let Hr = /* @__PURE__ */ new WeakMap();
function ws(e, t) {
  const n = Hr.get(e);
  return n ? (Hr.delete(e), n(t)) : Promise.resolve();
}
function jr(e, t, ...n) {
  var r = e, a = Fl, i;
  hr(() => {
    a !== (a = t()) && (i && (ht(i), i = null), i = Gt(() => (
      /** @type {SnippetFn} */
      a(r, ...n)
    )));
  }, cr);
}
function le(e, t, [n, r] = [0, 0]) {
  var a = e, i = null, s = null, o = Ie, u = n > 0 ? cr : 0, f = !1;
  const v = (d, g = !0) => {
    f = !0, c(g, d);
  }, c = (d, g) => {
    o !== (o = d) && (o ? (i ? Yn(i) : g && (i = Gt(() => g(a))), s && Vn(s, () => {
      s = null;
    })) : (s ? Yn(s) : g && (s = Gt(() => g(a, [n + 1, r]))), i && Vn(i, () => {
      i = null;
    })));
  };
  hr(() => {
    f = !1, t(v), f || c(null, null);
  }, u);
}
function ye(e, t) {
  return t;
}
function ys(e, t, n, r) {
  for (var a = [], i = t.length, s = 0; s < i; s++)
    aa(t[s].e, a, !0);
  var o = i > 0 && a.length === 0 && n !== null;
  if (o) {
    var u = (
      /** @type {Element} */
      /** @type {Element} */
      n.parentNode
    );
    Jl(u), u.append(
      /** @type {Element} */
      n
    ), r.clear(), mt(e, t[0].prev, t[i - 1].next);
  }
  Pi(a, () => {
    for (var f = 0; f < i; f++) {
      var v = t[f];
      o || (r.delete(v.k), mt(e, v.prev, v.next)), ht(v.e, !o);
    }
  });
}
function ke(e, t, n, r, a, i = null) {
  var s = e, o = { flags: t, items: /* @__PURE__ */ new Map(), first: null }, u = (t & gi) !== 0;
  if (u) {
    var f = (
      /** @type {Element} */
      e
    );
    s = f.appendChild(vr());
  }
  var v = null, c = !1, d = /* @__PURE__ */ Gl(() => {
    var g = n();
    return or(g) ? g : g == null ? [] : ea(g);
  });
  hr(() => {
    var g = l(d), h = g.length;
    c && h === 0 || (c = h === 0, ks(g, o, s, a, t, r, n), i !== null && (h === 0 ? v ? Yn(v) : v = Gt(() => i(s)) : v !== null && Vn(v, () => {
      v = null;
    })), l(d));
  });
}
function ks(e, t, n, r, a, i, s) {
  var q, A, N, Y;
  var o = (a & ml) !== 0, u = (a & (Jr | $r)) !== 0, f = e.length, v = t.items, c = t.first, d = c, g, h = null, _, w = [], T = [], k, p, y, S;
  if (o)
    for (S = 0; S < f; S += 1)
      k = e[S], p = i(k, S), y = v.get(p), y !== void 0 && ((q = y.a) == null || q.measure(), (_ ?? (_ = /* @__PURE__ */ new Set())).add(y));
  for (S = 0; S < f; S += 1) {
    if (k = e[S], p = i(k, S), y = v.get(p), y === void 0) {
      var C = d ? (
        /** @type {TemplateNode} */
        d.e.nodes_start
      ) : n;
      h = Ts(
        C,
        t,
        h,
        h === null ? t.first : h.next,
        k,
        p,
        S,
        r,
        a,
        s
      ), v.set(p, h), w = [], T = [], d = h.next;
      continue;
    }
    if (u && Ms(y, k, S, a), (y.e.f & vt) !== 0 && (Yn(y.e), o && ((A = y.a) == null || A.unfix(), (_ ?? (_ = /* @__PURE__ */ new Set())).delete(y))), y !== d) {
      if (g !== void 0 && g.has(y)) {
        if (w.length < T.length) {
          var z = T[0], H;
          h = z.prev;
          var V = w[0], J = w[w.length - 1];
          for (H = 0; H < w.length; H += 1)
            qa(w[H], z, n);
          for (H = 0; H < T.length; H += 1)
            g.delete(T[H]);
          mt(t, V.prev, J.next), mt(t, h, V), mt(t, J, z), d = z, h = J, S -= 1, w = [], T = [];
        } else
          g.delete(y), qa(y, d, n), mt(t, y.prev, y.next), mt(t, y, h === null ? t.first : h.next), mt(t, h, y), h = y;
        continue;
      }
      for (w = [], T = []; d !== null && d.k !== p; )
        (d.e.f & vt) === 0 && (g ?? (g = /* @__PURE__ */ new Set())).add(d), T.push(d), d = d.next;
      if (d === null)
        continue;
      y = d;
    }
    w.push(y), h = y, d = y.next;
  }
  if (d !== null || g !== void 0) {
    for (var E = g === void 0 ? [] : ea(g); d !== null; )
      (d.e.f & vt) === 0 && E.push(d), d = d.next;
    var R = E.length;
    if (R > 0) {
      var L = (a & gi) !== 0 && f === 0 ? n : null;
      if (o) {
        for (S = 0; S < R; S += 1)
          (N = E[S].a) == null || N.measure();
        for (S = 0; S < R; S += 1)
          (Y = E[S].a) == null || Y.fix();
      }
      ys(t, E, L, v);
    }
  }
  o && ia(() => {
    var D;
    if (_ !== void 0)
      for (y of _)
        (D = y.a) == null || D.apply();
  }), be.first = t.first && t.first.e, be.last = h && h.e;
}
function Ms(e, t, n, r) {
  (r & Jr) !== 0 && Ir(e.v, t), (r & $r) !== 0 ? Ir(
    /** @type {Value<number>} */
    e.i,
    n
  ) : e.i = n;
}
function Ts(e, t, n, r, a, i, s, o, u, f) {
  var v = (u & Jr) !== 0, c = (u & xl) === 0, d = v ? c ? /* @__PURE__ */ Ti(a) : Wn(a) : a, g = (u & $r) === 0 ? s : Wn(s), h = {
    i: g,
    v: d,
    k: i,
    a: null,
    // @ts-expect-error
    e: null,
    prev: n,
    next: r
  };
  try {
    return h.e = Gt(() => o(e, d, g, f), Zl), h.e.prev = n && n.e, h.e.next = r && r.e, n === null ? t.first = h : (n.next = h, n.e.next = h.e), r !== null && (r.prev = h, r.e.prev = h.e), h;
  } finally {
  }
}
function qa(e, t, n) {
  for (var r = e.next ? (
    /** @type {TemplateNode} */
    e.next.e.nodes_start
  ) : n, a = t ? (
    /** @type {TemplateNode} */
    t.e.nodes_start
  ) : n, i = (
    /** @type {TemplateNode} */
    e.e.nodes_start
  ); i !== r; ) {
    var s = (
      /** @type {TemplateNode} */
      /* @__PURE__ */ gr(i)
    );
    a.before(i), i = s;
  }
}
function mt(e, t, n) {
  t === null ? e.first = n : (t.next = n, t.e.next = n && n.e), n !== null && (n.prev = t, n.e.prev = t && t.e);
}
function Vi(e) {
  var t, n, r = "";
  if (typeof e == "string" || typeof e == "number") r += e;
  else if (typeof e == "object") if (Array.isArray(e)) {
    var a = e.length;
    for (t = 0; t < a; t++) e[t] && (n = Vi(e[t])) && (r && (r += " "), r += n);
  } else for (n in e) e[n] && (r && (r += " "), r += n);
  return r;
}
function As() {
  for (var e, t, n = 0, r = "", a = arguments.length; n < a; n++) (e = arguments[n]) && (t = Vi(e)) && (r && (r += " "), r += t);
  return r;
}
function Ss(e) {
  return typeof e == "object" ? As(e) : e ?? "";
}
const Pa = [...` 	
\r\f \v\uFEFF`];
function Es(e, t, n) {
  var r = e == null ? "" : "" + e;
  if (t && (r = r ? r + " " + t : t), n) {
    for (var a in n)
      if (n[a])
        r = r ? r + " " + a : a;
      else if (r.length)
        for (var i = a.length, s = 0; (s = r.indexOf(a, s)) >= 0; ) {
          var o = s + i;
          (s === 0 || Pa.includes(r[s - 1])) && (o === r.length || Pa.includes(r[o])) ? r = (s === 0 ? "" : r.substring(0, s)) + r.substring(o + 1) : s = o;
        }
  }
  return r === "" ? null : r;
}
function Ra(e, t = !1) {
  var n = t ? " !important;" : ";", r = "";
  for (var a in e) {
    var i = e[a];
    i != null && i !== "" && (r += " " + a + ": " + i + n);
  }
  return r;
}
function Lr(e) {
  return e[0] !== "-" || e[1] !== "-" ? e.toLowerCase() : e;
}
function Ls(e, t) {
  if (t) {
    var n = "", r, a;
    if (Array.isArray(t) ? (r = t[0], a = t[1]) : r = t, e) {
      e = String(e).replaceAll(/\s*\/\*.*?\*\/\s*/g, "").trim();
      var i = !1, s = 0, o = !1, u = [];
      r && u.push(...Object.keys(r).map(Lr)), a && u.push(...Object.keys(a).map(Lr));
      var f = 0, v = -1;
      const _ = e.length;
      for (var c = 0; c < _; c++) {
        var d = e[c];
        if (o ? d === "/" && e[c - 1] === "*" && (o = !1) : i ? i === d && (i = !1) : d === "/" && e[c + 1] === "*" ? o = !0 : d === '"' || d === "'" ? i = d : d === "(" ? s++ : d === ")" && s--, !o && i === !1 && s === 0) {
          if (d === ":" && v === -1)
            v = c;
          else if (d === ";" || c === _ - 1) {
            if (v !== -1) {
              var g = Lr(e.substring(f, v).trim());
              if (!u.includes(g)) {
                d !== ";" && c++;
                var h = e.substring(f, c).trim();
                n += " " + h + ";";
              }
            }
            f = c + 1, v = -1;
          }
        }
      }
    }
    return r && (n += Ra(r)), a && (n += Ra(a, !0)), n = n.trim(), n === "" ? null : n;
  }
  return e == null ? null : String(e);
}
function qe(e, t, n, r, a, i) {
  var s = e.__className;
  if (s !== n || s === void 0) {
    var o = Es(n, r, i);
    o == null ? e.removeAttribute("class") : e.className = o, e.__className = n;
  } else if (i && a !== i)
    for (var u in i) {
      var f = !!i[u];
      (a == null || f !== !!a[u]) && e.classList.toggle(u, f);
    }
  return i;
}
function Nr(e, t = {}, n, r) {
  for (var a in n) {
    var i = n[a];
    t[a] !== i && (n[a] == null ? e.style.removeProperty(a) : e.style.setProperty(a, i, r));
  }
}
function Be(e, t, n, r) {
  var a = e.__style;
  if (a !== t) {
    var i = Ls(t, r);
    i == null ? e.removeAttribute("style") : e.style.cssText = i, e.__style = t;
  } else r && (Array.isArray(r) ? (Nr(e, n == null ? void 0 : n[0], r[0]), Nr(e, n == null ? void 0 : n[1], r[1], "important")) : Nr(e, n, r));
  return r;
}
function Ot(e, t, n) {
  if (e.multiple) {
    if (t == null)
      return;
    if (!or(t))
      return Kl();
    for (var r of e.options)
      r.selected = t.includes(un(r));
    return;
  }
  for (r of e.options) {
    var a = un(r);
    if (Xl(a, t)) {
      r.selected = !0;
      return;
    }
  }
  (!n || t !== void 0) && (e.selectedIndex = -1);
}
function Cn(e, t) {
  let n = !0;
  tn(() => {
    t && Ot(e, Ct(t), n), n = !1;
    var r = new MutationObserver(() => {
      var a = e.__value;
      Ot(e, a);
    });
    return r.observe(e, {
      // Listen to option element changes
      childList: !0,
      subtree: !0,
      // because of <optgroup>
      // Listen to option element value attribute changes
      // (doesn't get notified of select value changes,
      // because that property is not reflected as an attribute)
      attributes: !0,
      attributeFilter: ["value"]
    }), () => {
      r.disconnect();
    };
  });
}
function Ns(e, t, n = t) {
  var r = !0;
  sa(e, "change", (a) => {
    var i = a ? "[selected]" : ":checked", s;
    if (e.multiple)
      s = [].map.call(e.querySelectorAll(i), un);
    else {
      var o = e.querySelector(i) ?? // will fall back to first non-disabled option if no option is selected
      e.querySelector("option:not([disabled])");
      s = o && un(o);
    }
    n(s);
  }), tn(() => {
    var a = t();
    if (Ot(e, a, r), r && a === void 0) {
      var i = e.querySelector(":checked");
      i !== null && (a = un(i), n(a));
    }
    e.__value = a, r = !1;
  }), Cn(e);
}
function un(e) {
  return "__value" in e ? e.__value : e.value;
}
const Fs = Symbol("is custom element"), Cs = Symbol("is html");
function za(e, t) {
  var n = oa(e);
  n.value === (n.value = // treat null and undefined the same for the initial value
  t ?? void 0) || // @ts-expect-error
  // `progress` elements always need their value set when it's `0`
  e.value === t && (t !== 0 || e.nodeName !== "PROGRESS") || (e.value = t ?? "");
}
function Ia(e, t) {
  var n = oa(e);
  n.checked !== (n.checked = // treat null and undefined the same for the initial value
  t ?? void 0) && (e.checked = t);
}
function M(e, t, n, r) {
  var a = oa(e);
  a[t] !== (a[t] = n) && (t === "loading" && (e[Rl] = n), n == null ? e.removeAttribute(t) : typeof n != "string" && qs(e).includes(t) ? e[t] = n : e.setAttribute(t, n));
}
function oa(e) {
  return (
    /** @type {Record<string | symbol, unknown>} **/
    // @ts-expect-error
    e.__attributes ?? (e.__attributes = {
      [Fs]: e.nodeName.includes("-"),
      [Cs]: e.namespaceURI === Tl
    })
  );
}
var Da = /* @__PURE__ */ new Map();
function qs(e) {
  var t = Da.get(e.nodeName);
  if (t) return t;
  Da.set(e.nodeName, t = []);
  for (var n, r = e, a = Element.prototype; a !== r; ) {
    n = El(r);
    for (var i in n)
      n[i].set && t.push(i);
    r = bi(r);
  }
  return t;
}
function mr(e, t, n = t) {
  sa(e, "input", (r) => {
    var a = r ? e.defaultValue : e.value;
    if (a = Fr(e) ? Cr(a) : a, n(a), a !== (a = t())) {
      var i = e.selectionStart, s = e.selectionEnd;
      e.value = a ?? "", s !== null && (e.selectionStart = i, e.selectionEnd = Math.min(s, e.value.length));
    }
  }), // If we are hydrating and the value has since changed,
  // then use the updated value from the input instead.
  // If defaultValue is set, then value == defaultValue
  // TODO Svelte 6: remove input.value check and set to empty string?
  Ct(t) == null && e.value && n(Fr(e) ? Cr(e.value) : e.value), ra(() => {
    var r = t();
    Fr(e) && r === Cr(e.value) || e.type === "date" && !r && !e.value || r !== e.value && (e.value = r ?? "");
  });
}
function vn(e, t, n = t) {
  sa(e, "change", (r) => {
    var a = r ? e.defaultChecked : e.checked;
    n(a);
  }), // If we are hydrating and the value has since changed,
  // then use the update value from the input instead.
  // If defaultChecked is set, then checked == defaultChecked
  Ct(t) == null && n(e.checked), ra(() => {
    var r = t();
    e.checked = !!r;
  });
}
function Fr(e) {
  var t = e.type;
  return t === "number" || t === "range";
}
function Cr(e) {
  return e === "" ? null : +e;
}
var xt, Wt, mn, lr, Yi;
const sr = class sr {
  /** @param {ResizeObserverOptions} options */
  constructor(t) {
    Fe(this, lr);
    /** */
    Fe(this, xt, /* @__PURE__ */ new WeakMap());
    /** @type {ResizeObserver | undefined} */
    Fe(this, Wt);
    /** @type {ResizeObserverOptions} */
    Fe(this, mn);
    We(this, mn, t);
  }
  /**
   * @param {Element} element
   * @param {(entry: ResizeObserverEntry) => any} listener
   */
  observe(t, n) {
    var r = oe(this, xt).get(t) || /* @__PURE__ */ new Set();
    return r.add(n), oe(this, xt).set(t, r), ka(this, lr, Yi).call(this).observe(t, oe(this, mn)), () => {
      var a = oe(this, xt).get(t);
      a.delete(n), a.size === 0 && (oe(this, xt).delete(t), oe(this, Wt).unobserve(t));
    };
  }
};
xt = new WeakMap(), Wt = new WeakMap(), mn = new WeakMap(), lr = new WeakSet(), Yi = function() {
  return oe(this, Wt) ?? We(this, Wt, new ResizeObserver(
    /** @param {any} entries */
    (t) => {
      for (var n of t) {
        sr.entries.set(n.target, n);
        for (var r of oe(this, xt).get(n.target) || [])
          r(n);
      }
    }
  ));
}, /** @static */
ya(sr, "entries", /* @__PURE__ */ new WeakMap());
let Wr = sr;
var Ps = /* @__PURE__ */ new Wr({
  box: "border-box"
});
function Qe(e, t, n) {
  var r = Ps.observe(e, () => n(e[t]));
  tn(() => (Ct(() => n(e[t])), r));
}
function Oa(e, t) {
  return e === t || (e == null ? void 0 : e[kt]) === t;
}
function Zn(e = {}, t, n, r) {
  return tn(() => {
    var a, i;
    return ra(() => {
      a = i, i = [], Ct(() => {
        e !== n(...i) && (t(e, ...i), a && Oa(n(...a), e) && t(null, ...a));
      });
    }), () => {
      ia(() => {
        i && Oa(n(...i), e) && t(null, ...i);
      });
    };
  }), e;
}
let An = !1;
function Rs(e) {
  var t = An;
  try {
    return An = !1, [e(), An];
  } finally {
    An = t;
  }
}
const zs = {
  get(e, t) {
    let n = e.props.length;
    for (; n--; ) {
      let r = e.props[n];
      if (ln(r) && (r = r()), typeof r == "object" && r !== null && t in r) return r[t];
    }
  },
  set(e, t, n) {
    let r = e.props.length;
    for (; r--; ) {
      let a = e.props[r];
      ln(a) && (a = a());
      const i = yt(a, t);
      if (i && i.set)
        return i.set(n), !0;
    }
    return !1;
  },
  getOwnPropertyDescriptor(e, t) {
    let n = e.props.length;
    for (; n--; ) {
      let r = e.props[n];
      if (ln(r) && (r = r()), typeof r == "object" && r !== null && t in r) {
        const a = yt(r, t);
        return a && !a.configurable && (a.configurable = !0), a;
      }
    }
  },
  has(e, t) {
    if (t === kt || t === xi) return !1;
    for (let n of e.props)
      if (ln(n) && (n = n()), n != null && t in n) return !0;
    return !1;
  },
  ownKeys(e) {
    const t = [];
    for (let n of e.props)
      if (ln(n) && (n = n()), !!n) {
        for (const r in n)
          t.includes(r) || t.push(r);
        for (const r of Object.getOwnPropertySymbols(n))
          t.includes(r) || t.push(r);
      }
    return t;
  }
};
function xr(...e) {
  return new Proxy({ props: e }, zs);
}
function Ba(e) {
  var t;
  return ((t = e.ctx) == null ? void 0 : t.d) ?? !1;
}
function F(e, t, n, r) {
  var S;
  var a = (n & pl) !== 0, i = !0, s = (n & yl) !== 0, o = (n & kl) !== 0, u = !1, f;
  s ? [f, u] = Rs(() => (
    /** @type {V} */
    e[t]
  )) : f = /** @type {V} */
  e[t];
  var v = kt in e || xi in e, c = s && (((S = yt(e, t)) == null ? void 0 : S.set) ?? (v && t in e && ((C) => e[t] = C))) || void 0, d = (
    /** @type {V} */
    r
  ), g = !0, h = !1, _ = () => (h = !0, g && (g = !1, o ? d = Ct(
    /** @type {() => V} */
    r
  ) : d = /** @type {V} */
  r), d);
  f === void 0 && r !== void 0 && (c && i && Hl(), f = _(), c && c(f));
  var w;
  if (w = () => {
    var C = (
      /** @type {V} */
      e[t]
    );
    return C === void 0 ? _() : (g = !0, h = !1, C);
  }, (n & wl) === 0)
    return w;
  if (c) {
    var T = e.$$legacy;
    return function(C, z) {
      return arguments.length > 0 ? ((!z || T || u) && c(z ? w() : C), C) : w();
    };
  }
  var k = !1, p = /* @__PURE__ */ Ti(f), y = /* @__PURE__ */ dr(() => {
    var C = w(), z = l(p);
    return k ? (k = !1, z) : p.v = C;
  });
  return s && l(y), a || (y.equals = na), function(C, z) {
    if (arguments.length > 0) {
      const H = z ? l(y) : s ? at(C) : C;
      if (!y.equals(H)) {
        if (k = !0, ee(p, H), h && d !== void 0 && (d = H), Ba(y))
          return C;
        Ct(() => l(y));
      }
      return C;
    }
    return Ba(y) ? y.v : l(y);
  };
}
var Is = (e, t, n) => t.changeTab(n()), Ds = /* @__PURE__ */ te('<li class="svelte-1qpu83q"><button> </button></li>'), Os = /* @__PURE__ */ te('<div class="svelte-1qpu83q"><ul class="svelte-1qpu83q"></ul></div>');
function Bs(e, t) {
  me(t, !0);
  const n = [
    { value: "overview", title: "Overview" },
    { value: "table", title: "Feature Table" },
    { value: "detail", title: "Feature Detail" }
  ];
  var r = Os(), a = b(r);
  ke(a, 21, () => n, ye, (i, s) => {
    let o = () => l(s).value, u = () => l(s).title;
    var f = Ds(), v = b(f);
    v.__click = [Is, t, o];
    let c;
    var d = b(v);
    ne(
      (g) => {
        c = qe(v, 1, "svelte-1qpu83q", null, c, g), de(d, u());
      },
      [
        () => ({
          "tab-selected": o() === t.selectedTab
        })
      ]
    ), I(i, f);
  }), I(e, r), xe();
}
Rt(["click"]);
var pt, ut, Vt;
class sn {
  constructor(t, n) {
    Fe(this, pt);
    Fe(this, ut);
    Fe(this, Vt);
    We(this, pt, t), We(this, ut, n), We(this, Vt, /* @__PURE__ */ se(at(oe(this, ut).get(oe(this, pt))))), oe(this, ut).on(`change:${oe(this, pt)}`, () => ee(oe(this, Vt), oe(this, ut).get(oe(this, pt)), !0));
  }
  get value() {
    return l(oe(this, Vt));
  }
  set value(t) {
    oe(this, ut).set(oe(this, pt), t), oe(this, ut).save_changes();
  }
}
pt = new WeakMap(), ut = new WeakMap(), Vt = new WeakMap();
var Yt;
class De {
  constructor(t, n) {
    Fe(this, Yt);
    We(this, Yt, /* @__PURE__ */ se(at(n.get(t)))), n.on(`change:${t}`, () => ee(oe(this, Yt), n.get(t), !0));
  }
  get value() {
    return l(oe(this, Yt));
  }
}
Yt = new WeakMap();
var ct, xn, pn, wn, yn;
class Hs {
  constructor(t) {
    Fe(this, ct);
    Fe(this, xn);
    Fe(this, pn);
    Fe(this, wn);
    Fe(this, yn);
    We(this, ct, new De("base_font_size", t)), We(this, xn, /* @__PURE__ */ x(() => oe(this, ct).value * 0.75)), We(this, pn, /* @__PURE__ */ x(() => oe(this, ct).value * 0.875)), We(this, wn, /* @__PURE__ */ x(() => oe(this, ct).value * 1.125)), We(this, yn, /* @__PURE__ */ x(() => oe(this, ct).value * 1.25));
  }
  get base() {
    return oe(this, ct).value;
  }
  get xs() {
    return l(oe(this, xn));
  }
  get sm() {
    return l(oe(this, pn));
  }
  get lg() {
    return l(oe(this, wn));
  }
  get xl() {
    return l(oe(this, yn));
  }
}
ct = new WeakMap(), xn = new WeakMap(), pn = new WeakMap(), wn = new WeakMap(), yn = new WeakMap();
let Xi, Se, Bt, St, ce, Vr, It, fn, Yr, rt, cn, Xr, qn, Dt, ae;
function js(e) {
  Xi = new De("height", e), new De("n_table_rows", e), Se = new De("dataset_info", e), Bt = new De("model_info", e), new De("sae_ids", e), new De("sae_id", e), St = new De("sae_data", e), ce = new sn("table_ranking_option", e), Vr = new sn("table_min_act_rate", e), It = new sn("table_page_index", e), fn = new De("max_table_page_index", e), new De("num_filtered_features", e), Yr = new De("table_features", e), rt = new De("detail_feature", e), cn = new sn("detail_feature_id", e), Xr = new De("can_inference", e), qn = new sn("inference_input", e), Dt = new De("inference_output", e), ae = new Hs(e);
}
var Ws = /* @__PURE__ */ we('<svg stroke-width="2" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" color="currentcolor"><path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentcolor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path><path d="M9 9C9 5.49997 14.5 5.5 14.5 9C14.5 11.5 12 10.9999 12 13.9999" stroke="currentcolor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path><path d="M12 18.01L12.01 17.9989" stroke="currentcolor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>');
function Ze(e, t) {
  me(t, !0);
  let n = F(t, "width", 19, () => ae.base), r = F(t, "height", 19, () => ae.base);
  var a = Ws();
  ne(() => {
    M(a, "width", n()), M(a, "height", r());
  }), I(e, a), xe();
}
var Xt;
class At {
  constructor(t) {
    Fe(this, Xt);
    We(this, Xt, /* @__PURE__ */ se(at(t)));
  }
  get value() {
    return l(oe(this, Xt));
  }
  set value(t) {
    ee(oe(this, Xt), t, !0);
  }
}
Xt = new WeakMap();
let fa, Pn, Rn, zn, In, Dn, On;
function Vs(e) {
  fa = new At(e), Pn = new At(!1), Rn = new At(!1), zn = new At(!1), In = new At(0), Dn = new At(!1), On = new At(!1);
}
function Ys(e) {
  e.preventDefault();
}
var Xs = /* @__PURE__ */ te('<div class="sae-tooltip-container svelte-1grq8y5"><button class="svelte-1grq8y5"><!></button> <div popover="auto" class="svelte-1grq8y5"><!></div></div>');
function Ye(e, t) {
  const n = bs();
  me(t, !0);
  let r = F(t, "position", 3, "auto");
  function a(z, H, V, J, E) {
    if (H === null || V === null)
      return 0;
    const R = z / 2, L = V.height / 2;
    return E === "right" || E === "left" ? V.top + L - R : E === "bottom" || E === "auto" && V.top - z < H.top ? V.bottom + J : V.top - z - J;
  }
  function i(z, H, V, J, E) {
    if (H === null || V === null)
      return 0;
    const R = z / 2, L = V.left + V.width / 2;
    return E === "right" || E === "auto" && L - R < H.left ? V.right + J : E === "left" || E === "auto" && L + R > H.right ? V.left - z - J : L - R;
  }
  const s = 4;
  let o = /* @__PURE__ */ se(void 0), u = /* @__PURE__ */ se(void 0), f = /* @__PURE__ */ se(0), v = /* @__PURE__ */ se(0), c = /* @__PURE__ */ se(null), d = /* @__PURE__ */ se(null), g = /* @__PURE__ */ x(() => a(l(v), l(d), l(c), s, r())), h = /* @__PURE__ */ x(() => i(l(f), l(d), l(c), s, r()));
  function _() {
    l(o) && l(u) && (ee(c, l(o).getBoundingClientRect(), !0), ee(d, fa.value.getBoundingClientRect(), !0), l(u).showPopover());
  }
  function w() {
    l(o) && l(u) && l(u).hidePopover();
  }
  var T = Xs(), k = b(T);
  k.__click = [Ys];
  var p = b(k);
  jr(p, () => t.trigger), Zn(k, (z) => ee(o, z), () => l(o));
  var y = m(k, 2);
  let S;
  var C = b(y);
  jr(C, () => t.content), Zn(y, (z) => ee(u, z), () => l(u)), ne(() => {
    M(k, "popovertarget", n), M(y, "id", n), S = Be(y, "", S, {
      top: `${l(g) ?? ""}px`,
      left: `${l(h) ?? ""}px`
    });
  }), Je("mouseenter", k, _), Je("mouseleave", k, w), Qe(y, "offsetWidth", (z) => ee(f, z)), Qe(y, "offsetHeight", (z) => ee(v, z)), I(e, T), xe();
}
Rt(["click"]);
function Bn(e, t) {
  return e == null || t == null ? NaN : e < t ? -1 : e > t ? 1 : e >= t ? 0 : NaN;
}
function Gi(e, t) {
  return e == null || t == null ? NaN : t < e ? -1 : t > e ? 1 : t >= e ? 0 : NaN;
}
function Ui(e) {
  let t, n, r;
  e.length !== 2 ? (t = Bn, n = (o, u) => Bn(e(o), u), r = (o, u) => e(o) - u) : (t = e === Bn || e === Gi ? e : Gs, n = e, r = e);
  function a(o, u, f = 0, v = o.length) {
    if (f < v) {
      if (t(u, u) !== 0) return v;
      do {
        const c = f + v >>> 1;
        n(o[c], u) < 0 ? f = c + 1 : v = c;
      } while (f < v);
    }
    return f;
  }
  function i(o, u, f = 0, v = o.length) {
    if (f < v) {
      if (t(u, u) !== 0) return v;
      do {
        const c = f + v >>> 1;
        n(o[c], u) <= 0 ? f = c + 1 : v = c;
      } while (f < v);
    }
    return f;
  }
  function s(o, u, f = 0, v = o.length) {
    const c = a(o, u, f, v - 1);
    return c > f && r(o[c - 1], u) > -r(o[c], u) ? c - 1 : c;
  }
  return { left: a, center: s, right: i };
}
function Gs() {
  return 0;
}
function Us(e) {
  return e === null ? NaN : +e;
}
const Ks = Ui(Bn), Zs = Ks.right;
Ui(Us).center;
function Qs(e, t) {
  let n, r;
  if (t === void 0)
    for (const a of e)
      a != null && (n === void 0 ? a >= a && (n = r = a) : (n > a && (n = a), r < a && (r = a)));
  else {
    let a = -1;
    for (let i of e)
      (i = t(i, ++a, e)) != null && (n === void 0 ? i >= i && (n = r = i) : (n > i && (n = i), r < i && (r = i)));
  }
  return [n, r];
}
class Ha extends Map {
  constructor(t, n = eo) {
    if (super(), Object.defineProperties(this, { _intern: { value: /* @__PURE__ */ new Map() }, _key: { value: n } }), t != null) for (const [r, a] of t) this.set(r, a);
  }
  get(t) {
    return super.get(ja(this, t));
  }
  has(t) {
    return super.has(ja(this, t));
  }
  set(t, n) {
    return super.set(Js(this, t), n);
  }
  delete(t) {
    return super.delete($s(this, t));
  }
}
function ja({ _intern: e, _key: t }, n) {
  const r = t(n);
  return e.has(r) ? e.get(r) : n;
}
function Js({ _intern: e, _key: t }, n) {
  const r = t(n);
  return e.has(r) ? e.get(r) : (e.set(r, n), n);
}
function $s({ _intern: e, _key: t }, n) {
  const r = t(n);
  return e.has(r) && (n = e.get(r), e.delete(r)), n;
}
function eo(e) {
  return e !== null && typeof e == "object" ? e.valueOf() : e;
}
const to = Math.sqrt(50), no = Math.sqrt(10), ro = Math.sqrt(2);
function Qn(e, t, n) {
  const r = (t - e) / Math.max(0, n), a = Math.floor(Math.log10(r)), i = r / Math.pow(10, a), s = i >= to ? 10 : i >= no ? 5 : i >= ro ? 2 : 1;
  let o, u, f;
  return a < 0 ? (f = Math.pow(10, -a) / s, o = Math.round(e * f), u = Math.round(t * f), o / f < e && ++o, u / f > t && --u, f = -f) : (f = Math.pow(10, a) * s, o = Math.round(e / f), u = Math.round(t / f), o * f < e && ++o, u * f > t && --u), u < o && 0.5 <= n && n < 2 ? Qn(e, t, n * 2) : [o, u, f];
}
function ao(e, t, n) {
  if (t = +t, e = +e, n = +n, !(n > 0)) return [];
  if (e === t) return [e];
  const r = t < e, [a, i, s] = r ? Qn(t, e, n) : Qn(e, t, n);
  if (!(i >= a)) return [];
  const o = i - a + 1, u = new Array(o);
  if (r)
    if (s < 0) for (let f = 0; f < o; ++f) u[f] = (i - f) / -s;
    else for (let f = 0; f < o; ++f) u[f] = (i - f) * s;
  else if (s < 0) for (let f = 0; f < o; ++f) u[f] = (a + f) / -s;
  else for (let f = 0; f < o; ++f) u[f] = (a + f) * s;
  return u;
}
function Gr(e, t, n) {
  return t = +t, e = +e, n = +n, Qn(e, t, n)[2];
}
function io(e, t, n) {
  t = +t, e = +e, n = +n;
  const r = t < e, a = r ? Gr(t, e, n) : Gr(e, t, n);
  return (r ? -1 : 1) * (a < 0 ? 1 / -a : a);
}
function lo(e, t) {
  let n;
  if (t === void 0)
    for (const r of e)
      r != null && (n < r || n === void 0 && r >= r) && (n = r);
  else {
    let r = -1;
    for (let a of e)
      (a = t(a, ++r, e)) != null && (n < a || n === void 0 && a >= a) && (n = a);
  }
  return n;
}
function so(e, t) {
  let n;
  if (t === void 0)
    for (const r of e)
      r != null && (n > r || n === void 0 && r >= r) && (n = r);
  else {
    let r = -1;
    for (let a of e)
      (a = t(a, ++r, e)) != null && (n > a || n === void 0 && a >= a) && (n = a);
  }
  return n;
}
function Ki(e, t = oo) {
  const n = [];
  let r, a = !1;
  for (const i of e)
    a && n.push(t(r, i)), r = i, a = !0;
  return n;
}
function oo(e, t) {
  return [e, t];
}
function ua(e, t, n) {
  e = +e, t = +t, n = (a = arguments.length) < 2 ? (t = e, e = 0, 1) : a < 3 ? 1 : +n;
  for (var r = -1, a = Math.max(0, Math.ceil((t - e) / n)) | 0, i = new Array(a); ++r < a; )
    i[r] = e + r * n;
  return i;
}
function fo(e) {
  if (!(i = e.length)) return [];
  for (var t = -1, n = so(e, uo), r = new Array(n); ++t < n; )
    for (var a = -1, i, s = r[t] = new Array(i); ++a < i; )
      s[a] = e[a][t];
  return r;
}
function uo(e) {
  return e.length;
}
function co() {
  return fo(arguments);
}
function ca(e, t) {
  switch (arguments.length) {
    case 0:
      break;
    case 1:
      this.range(e);
      break;
    default:
      this.range(t).domain(e);
      break;
  }
  return this;
}
function Zi(e, t) {
  switch (arguments.length) {
    case 0:
      break;
    case 1: {
      typeof e == "function" ? this.interpolator(e) : this.range(e);
      break;
    }
    default: {
      this.domain(e), typeof t == "function" ? this.interpolator(t) : this.range(t);
      break;
    }
  }
  return this;
}
const Wa = Symbol("implicit");
function Qi() {
  var e = new Ha(), t = [], n = [], r = Wa;
  function a(i) {
    let s = e.get(i);
    if (s === void 0) {
      if (r !== Wa) return r;
      e.set(i, s = t.push(i) - 1);
    }
    return n[s % n.length];
  }
  return a.domain = function(i) {
    if (!arguments.length) return t.slice();
    t = [], e = new Ha();
    for (const s of i)
      e.has(s) || e.set(s, t.push(s) - 1);
    return a;
  }, a.range = function(i) {
    return arguments.length ? (n = Array.from(i), a) : n.slice();
  }, a.unknown = function(i) {
    return arguments.length ? (r = i, a) : r;
  }, a.copy = function() {
    return Qi(t, n).unknown(r);
  }, ca.apply(a, arguments), a;
}
function Jn() {
  var e = Qi().unknown(void 0), t = e.domain, n = e.range, r = 0, a = 1, i, s, o = !1, u = 0, f = 0, v = 0.5;
  delete e.unknown;
  function c() {
    var d = t().length, g = a < r, h = g ? a : r, _ = g ? r : a;
    i = (_ - h) / Math.max(1, d - u + f * 2), o && (i = Math.floor(i)), h += (_ - h - i * (d - u)) * v, s = i * (1 - u), o && (h = Math.round(h), s = Math.round(s));
    var w = ua(d).map(function(T) {
      return h + i * T;
    });
    return n(g ? w.reverse() : w);
  }
  return e.domain = function(d) {
    return arguments.length ? (t(d), c()) : t();
  }, e.range = function(d) {
    return arguments.length ? ([r, a] = d, r = +r, a = +a, c()) : [r, a];
  }, e.rangeRound = function(d) {
    return [r, a] = d, r = +r, a = +a, o = !0, c();
  }, e.bandwidth = function() {
    return s;
  }, e.step = function() {
    return i;
  }, e.round = function(d) {
    return arguments.length ? (o = !!d, c()) : o;
  }, e.padding = function(d) {
    return arguments.length ? (u = Math.min(1, f = +d), c()) : u;
  }, e.paddingInner = function(d) {
    return arguments.length ? (u = Math.min(1, d), c()) : u;
  }, e.paddingOuter = function(d) {
    return arguments.length ? (f = +d, c()) : f;
  }, e.align = function(d) {
    return arguments.length ? (v = Math.max(0, Math.min(1, d)), c()) : v;
  }, e.copy = function() {
    return Jn(t(), [r, a]).round(o).paddingInner(u).paddingOuter(f).align(v);
  }, ca.apply(c(), arguments);
}
function da(e, t, n) {
  e.prototype = t.prototype = n, n.constructor = e;
}
function Ji(e, t) {
  var n = Object.create(e.prototype);
  for (var r in t) n[r] = t[r];
  return n;
}
function Mn() {
}
var gn = 0.7, $n = 1 / gn, Ht = "\\s*([+-]?\\d+)\\s*", hn = "\\s*([+-]?(?:\\d*\\.)?\\d+(?:[eE][+-]?\\d+)?)\\s*", st = "\\s*([+-]?(?:\\d*\\.)?\\d+(?:[eE][+-]?\\d+)?)%\\s*", vo = /^#([0-9a-f]{3,8})$/, go = new RegExp(`^rgb\\(${Ht},${Ht},${Ht}\\)$`), ho = new RegExp(`^rgb\\(${st},${st},${st}\\)$`), bo = new RegExp(`^rgba\\(${Ht},${Ht},${Ht},${hn}\\)$`), _o = new RegExp(`^rgba\\(${st},${st},${st},${hn}\\)$`), mo = new RegExp(`^hsl\\(${hn},${st},${st}\\)$`), xo = new RegExp(`^hsla\\(${hn},${st},${st},${hn}\\)$`), Va = {
  aliceblue: 15792383,
  antiquewhite: 16444375,
  aqua: 65535,
  aquamarine: 8388564,
  azure: 15794175,
  beige: 16119260,
  bisque: 16770244,
  black: 0,
  blanchedalmond: 16772045,
  blue: 255,
  blueviolet: 9055202,
  brown: 10824234,
  burlywood: 14596231,
  cadetblue: 6266528,
  chartreuse: 8388352,
  chocolate: 13789470,
  coral: 16744272,
  cornflowerblue: 6591981,
  cornsilk: 16775388,
  crimson: 14423100,
  cyan: 65535,
  darkblue: 139,
  darkcyan: 35723,
  darkgoldenrod: 12092939,
  darkgray: 11119017,
  darkgreen: 25600,
  darkgrey: 11119017,
  darkkhaki: 12433259,
  darkmagenta: 9109643,
  darkolivegreen: 5597999,
  darkorange: 16747520,
  darkorchid: 10040012,
  darkred: 9109504,
  darksalmon: 15308410,
  darkseagreen: 9419919,
  darkslateblue: 4734347,
  darkslategray: 3100495,
  darkslategrey: 3100495,
  darkturquoise: 52945,
  darkviolet: 9699539,
  deeppink: 16716947,
  deepskyblue: 49151,
  dimgray: 6908265,
  dimgrey: 6908265,
  dodgerblue: 2003199,
  firebrick: 11674146,
  floralwhite: 16775920,
  forestgreen: 2263842,
  fuchsia: 16711935,
  gainsboro: 14474460,
  ghostwhite: 16316671,
  gold: 16766720,
  goldenrod: 14329120,
  gray: 8421504,
  green: 32768,
  greenyellow: 11403055,
  grey: 8421504,
  honeydew: 15794160,
  hotpink: 16738740,
  indianred: 13458524,
  indigo: 4915330,
  ivory: 16777200,
  khaki: 15787660,
  lavender: 15132410,
  lavenderblush: 16773365,
  lawngreen: 8190976,
  lemonchiffon: 16775885,
  lightblue: 11393254,
  lightcoral: 15761536,
  lightcyan: 14745599,
  lightgoldenrodyellow: 16448210,
  lightgray: 13882323,
  lightgreen: 9498256,
  lightgrey: 13882323,
  lightpink: 16758465,
  lightsalmon: 16752762,
  lightseagreen: 2142890,
  lightskyblue: 8900346,
  lightslategray: 7833753,
  lightslategrey: 7833753,
  lightsteelblue: 11584734,
  lightyellow: 16777184,
  lime: 65280,
  limegreen: 3329330,
  linen: 16445670,
  magenta: 16711935,
  maroon: 8388608,
  mediumaquamarine: 6737322,
  mediumblue: 205,
  mediumorchid: 12211667,
  mediumpurple: 9662683,
  mediumseagreen: 3978097,
  mediumslateblue: 8087790,
  mediumspringgreen: 64154,
  mediumturquoise: 4772300,
  mediumvioletred: 13047173,
  midnightblue: 1644912,
  mintcream: 16121850,
  mistyrose: 16770273,
  moccasin: 16770229,
  navajowhite: 16768685,
  navy: 128,
  oldlace: 16643558,
  olive: 8421376,
  olivedrab: 7048739,
  orange: 16753920,
  orangered: 16729344,
  orchid: 14315734,
  palegoldenrod: 15657130,
  palegreen: 10025880,
  paleturquoise: 11529966,
  palevioletred: 14381203,
  papayawhip: 16773077,
  peachpuff: 16767673,
  peru: 13468991,
  pink: 16761035,
  plum: 14524637,
  powderblue: 11591910,
  purple: 8388736,
  rebeccapurple: 6697881,
  red: 16711680,
  rosybrown: 12357519,
  royalblue: 4286945,
  saddlebrown: 9127187,
  salmon: 16416882,
  sandybrown: 16032864,
  seagreen: 3050327,
  seashell: 16774638,
  sienna: 10506797,
  silver: 12632256,
  skyblue: 8900331,
  slateblue: 6970061,
  slategray: 7372944,
  slategrey: 7372944,
  snow: 16775930,
  springgreen: 65407,
  steelblue: 4620980,
  tan: 13808780,
  teal: 32896,
  thistle: 14204888,
  tomato: 16737095,
  turquoise: 4251856,
  violet: 15631086,
  wheat: 16113331,
  white: 16777215,
  whitesmoke: 16119285,
  yellow: 16776960,
  yellowgreen: 10145074
};
da(Mn, bn, {
  copy(e) {
    return Object.assign(new this.constructor(), this, e);
  },
  displayable() {
    return this.rgb().displayable();
  },
  hex: Ya,
  // Deprecated! Use color.formatHex.
  formatHex: Ya,
  formatHex8: po,
  formatHsl: wo,
  formatRgb: Xa,
  toString: Xa
});
function Ya() {
  return this.rgb().formatHex();
}
function po() {
  return this.rgb().formatHex8();
}
function wo() {
  return $i(this).formatHsl();
}
function Xa() {
  return this.rgb().formatRgb();
}
function bn(e) {
  var t, n;
  return e = (e + "").trim().toLowerCase(), (t = vo.exec(e)) ? (n = t[1].length, t = parseInt(t[1], 16), n === 6 ? Ga(t) : n === 3 ? new Oe(t >> 8 & 15 | t >> 4 & 240, t >> 4 & 15 | t & 240, (t & 15) << 4 | t & 15, 1) : n === 8 ? Sn(t >> 24 & 255, t >> 16 & 255, t >> 8 & 255, (t & 255) / 255) : n === 4 ? Sn(t >> 12 & 15 | t >> 8 & 240, t >> 8 & 15 | t >> 4 & 240, t >> 4 & 15 | t & 240, ((t & 15) << 4 | t & 15) / 255) : null) : (t = go.exec(e)) ? new Oe(t[1], t[2], t[3], 1) : (t = ho.exec(e)) ? new Oe(t[1] * 255 / 100, t[2] * 255 / 100, t[3] * 255 / 100, 1) : (t = bo.exec(e)) ? Sn(t[1], t[2], t[3], t[4]) : (t = _o.exec(e)) ? Sn(t[1] * 255 / 100, t[2] * 255 / 100, t[3] * 255 / 100, t[4]) : (t = mo.exec(e)) ? Za(t[1], t[2] / 100, t[3] / 100, 1) : (t = xo.exec(e)) ? Za(t[1], t[2] / 100, t[3] / 100, t[4]) : Va.hasOwnProperty(e) ? Ga(Va[e]) : e === "transparent" ? new Oe(NaN, NaN, NaN, 0) : null;
}
function Ga(e) {
  return new Oe(e >> 16 & 255, e >> 8 & 255, e & 255, 1);
}
function Sn(e, t, n, r) {
  return r <= 0 && (e = t = n = NaN), new Oe(e, t, n, r);
}
function yo(e) {
  return e instanceof Mn || (e = bn(e)), e ? (e = e.rgb(), new Oe(e.r, e.g, e.b, e.opacity)) : new Oe();
}
function er(e, t, n, r) {
  return arguments.length === 1 ? yo(e) : new Oe(e, t, n, r ?? 1);
}
function Oe(e, t, n, r) {
  this.r = +e, this.g = +t, this.b = +n, this.opacity = +r;
}
da(Oe, er, Ji(Mn, {
  brighter(e) {
    return e = e == null ? $n : Math.pow($n, e), new Oe(this.r * e, this.g * e, this.b * e, this.opacity);
  },
  darker(e) {
    return e = e == null ? gn : Math.pow(gn, e), new Oe(this.r * e, this.g * e, this.b * e, this.opacity);
  },
  rgb() {
    return this;
  },
  clamp() {
    return new Oe(Nt(this.r), Nt(this.g), Nt(this.b), tr(this.opacity));
  },
  displayable() {
    return -0.5 <= this.r && this.r < 255.5 && -0.5 <= this.g && this.g < 255.5 && -0.5 <= this.b && this.b < 255.5 && 0 <= this.opacity && this.opacity <= 1;
  },
  hex: Ua,
  // Deprecated! Use color.formatHex.
  formatHex: Ua,
  formatHex8: ko,
  formatRgb: Ka,
  toString: Ka
}));
function Ua() {
  return `#${Et(this.r)}${Et(this.g)}${Et(this.b)}`;
}
function ko() {
  return `#${Et(this.r)}${Et(this.g)}${Et(this.b)}${Et((isNaN(this.opacity) ? 1 : this.opacity) * 255)}`;
}
function Ka() {
  const e = tr(this.opacity);
  return `${e === 1 ? "rgb(" : "rgba("}${Nt(this.r)}, ${Nt(this.g)}, ${Nt(this.b)}${e === 1 ? ")" : `, ${e})`}`;
}
function tr(e) {
  return isNaN(e) ? 1 : Math.max(0, Math.min(1, e));
}
function Nt(e) {
  return Math.max(0, Math.min(255, Math.round(e) || 0));
}
function Et(e) {
  return e = Nt(e), (e < 16 ? "0" : "") + e.toString(16);
}
function Za(e, t, n, r) {
  return r <= 0 ? e = t = n = NaN : n <= 0 || n >= 1 ? e = t = NaN : t <= 0 && (e = NaN), new et(e, t, n, r);
}
function $i(e) {
  if (e instanceof et) return new et(e.h, e.s, e.l, e.opacity);
  if (e instanceof Mn || (e = bn(e)), !e) return new et();
  if (e instanceof et) return e;
  e = e.rgb();
  var t = e.r / 255, n = e.g / 255, r = e.b / 255, a = Math.min(t, n, r), i = Math.max(t, n, r), s = NaN, o = i - a, u = (i + a) / 2;
  return o ? (t === i ? s = (n - r) / o + (n < r) * 6 : n === i ? s = (r - t) / o + 2 : s = (t - n) / o + 4, o /= u < 0.5 ? i + a : 2 - i - a, s *= 60) : o = u > 0 && u < 1 ? 0 : s, new et(s, o, u, e.opacity);
}
function Mo(e, t, n, r) {
  return arguments.length === 1 ? $i(e) : new et(e, t, n, r ?? 1);
}
function et(e, t, n, r) {
  this.h = +e, this.s = +t, this.l = +n, this.opacity = +r;
}
da(et, Mo, Ji(Mn, {
  brighter(e) {
    return e = e == null ? $n : Math.pow($n, e), new et(this.h, this.s, this.l * e, this.opacity);
  },
  darker(e) {
    return e = e == null ? gn : Math.pow(gn, e), new et(this.h, this.s, this.l * e, this.opacity);
  },
  rgb() {
    var e = this.h % 360 + (this.h < 0) * 360, t = isNaN(e) || isNaN(this.s) ? 0 : this.s, n = this.l, r = n + (n < 0.5 ? n : 1 - n) * t, a = 2 * n - r;
    return new Oe(
      qr(e >= 240 ? e - 240 : e + 120, a, r),
      qr(e, a, r),
      qr(e < 120 ? e + 240 : e - 120, a, r),
      this.opacity
    );
  },
  clamp() {
    return new et(Qa(this.h), En(this.s), En(this.l), tr(this.opacity));
  },
  displayable() {
    return (0 <= this.s && this.s <= 1 || isNaN(this.s)) && 0 <= this.l && this.l <= 1 && 0 <= this.opacity && this.opacity <= 1;
  },
  formatHsl() {
    const e = tr(this.opacity);
    return `${e === 1 ? "hsl(" : "hsla("}${Qa(this.h)}, ${En(this.s) * 100}%, ${En(this.l) * 100}%${e === 1 ? ")" : `, ${e})`}`;
  }
}));
function Qa(e) {
  return e = (e || 0) % 360, e < 0 ? e + 360 : e;
}
function En(e) {
  return Math.max(0, Math.min(1, e || 0));
}
function qr(e, t, n) {
  return (e < 60 ? t + (n - t) * e / 60 : e < 180 ? n : e < 240 ? t + (n - t) * (240 - e) / 60 : t) * 255;
}
function To(e, t, n, r, a) {
  var i = e * e, s = i * e;
  return ((1 - 3 * e + 3 * i - s) * t + (4 - 6 * i + 3 * s) * n + (1 + 3 * e + 3 * i - 3 * s) * r + s * a) / 6;
}
function Ao(e) {
  var t = e.length - 1;
  return function(n) {
    var r = n <= 0 ? n = 0 : n >= 1 ? (n = 1, t - 1) : Math.floor(n * t), a = e[r], i = e[r + 1], s = r > 0 ? e[r - 1] : 2 * a - i, o = r < t - 1 ? e[r + 2] : 2 * i - a;
    return To((n - r / t) * t, s, a, i, o);
  };
}
const va = (e) => () => e;
function So(e, t) {
  return function(n) {
    return e + n * t;
  };
}
function Eo(e, t, n) {
  return e = Math.pow(e, n), t = Math.pow(t, n) - e, n = 1 / n, function(r) {
    return Math.pow(e + r * t, n);
  };
}
function Lo(e) {
  return (e = +e) == 1 ? el : function(t, n) {
    return n - t ? Eo(t, n, e) : va(isNaN(t) ? n : t);
  };
}
function el(e, t) {
  var n = t - e;
  return n ? So(e, n) : va(isNaN(e) ? t : e);
}
const Ja = function e(t) {
  var n = Lo(t);
  function r(a, i) {
    var s = n((a = er(a)).r, (i = er(i)).r), o = n(a.g, i.g), u = n(a.b, i.b), f = el(a.opacity, i.opacity);
    return function(v) {
      return a.r = s(v), a.g = o(v), a.b = u(v), a.opacity = f(v), a + "";
    };
  }
  return r.gamma = e, r;
}(1);
function No(e) {
  return function(t) {
    var n = t.length, r = new Array(n), a = new Array(n), i = new Array(n), s, o;
    for (s = 0; s < n; ++s)
      o = er(t[s]), r[s] = o.r || 0, a[s] = o.g || 0, i[s] = o.b || 0;
    return r = e(r), a = e(a), i = e(i), o.opacity = 1, function(u) {
      return o.r = r(u), o.g = a(u), o.b = i(u), o + "";
    };
  };
}
var Fo = No(Ao);
function Co(e, t) {
  t || (t = []);
  var n = e ? Math.min(t.length, e.length) : 0, r = t.slice(), a;
  return function(i) {
    for (a = 0; a < n; ++a) r[a] = e[a] * (1 - i) + t[a] * i;
    return r;
  };
}
function qo(e) {
  return ArrayBuffer.isView(e) && !(e instanceof DataView);
}
function Po(e, t) {
  var n = t ? t.length : 0, r = e ? Math.min(n, e.length) : 0, a = new Array(r), i = new Array(n), s;
  for (s = 0; s < r; ++s) a[s] = rn(e[s], t[s]);
  for (; s < n; ++s) i[s] = t[s];
  return function(o) {
    for (s = 0; s < r; ++s) i[s] = a[s](o);
    return i;
  };
}
function Ro(e, t) {
  var n = /* @__PURE__ */ new Date();
  return e = +e, t = +t, function(r) {
    return n.setTime(e * (1 - r) + t * r), n;
  };
}
function nr(e, t) {
  return e = +e, t = +t, function(n) {
    return e * (1 - n) + t * n;
  };
}
function zo(e, t) {
  var n = {}, r = {}, a;
  (e === null || typeof e != "object") && (e = {}), (t === null || typeof t != "object") && (t = {});
  for (a in t)
    a in e ? n[a] = rn(e[a], t[a]) : r[a] = t[a];
  return function(i) {
    for (a in n) r[a] = n[a](i);
    return r;
  };
}
var Ur = /[-+]?(?:\d+\.?\d*|\.?\d+)(?:[eE][-+]?\d+)?/g, Pr = new RegExp(Ur.source, "g");
function Io(e) {
  return function() {
    return e;
  };
}
function Do(e) {
  return function(t) {
    return e(t) + "";
  };
}
function Oo(e, t) {
  var n = Ur.lastIndex = Pr.lastIndex = 0, r, a, i, s = -1, o = [], u = [];
  for (e = e + "", t = t + ""; (r = Ur.exec(e)) && (a = Pr.exec(t)); )
    (i = a.index) > n && (i = t.slice(n, i), o[s] ? o[s] += i : o[++s] = i), (r = r[0]) === (a = a[0]) ? o[s] ? o[s] += a : o[++s] = a : (o[++s] = null, u.push({ i: s, x: nr(r, a) })), n = Pr.lastIndex;
  return n < t.length && (i = t.slice(n), o[s] ? o[s] += i : o[++s] = i), o.length < 2 ? u[0] ? Do(u[0].x) : Io(t) : (t = u.length, function(f) {
    for (var v = 0, c; v < t; ++v) o[(c = u[v]).i] = c.x(f);
    return o.join("");
  });
}
function rn(e, t) {
  var n = typeof t, r;
  return t == null || n === "boolean" ? va(t) : (n === "number" ? nr : n === "string" ? (r = bn(t)) ? (t = r, Ja) : Oo : t instanceof bn ? Ja : t instanceof Date ? Ro : qo(t) ? Co : Array.isArray(t) ? Po : typeof t.valueOf != "function" && typeof t.toString != "function" || isNaN(t) ? zo : nr)(e, t);
}
function ga(e, t) {
  return e = +e, t = +t, function(n) {
    return Math.round(e * (1 - n) + t * n);
  };
}
function Bo(e, t) {
  t === void 0 && (t = e, e = rn);
  for (var n = 0, r = t.length - 1, a = t[0], i = new Array(r < 0 ? 0 : r); n < r; ) i[n] = e(a, a = t[++n]);
  return function(s) {
    var o = Math.max(0, Math.min(r - 1, Math.floor(s *= r)));
    return i[o](s - o);
  };
}
function Ho(e) {
  return function() {
    return e;
  };
}
function jo(e) {
  return +e;
}
var $a = [0, 1];
function lt(e) {
  return e;
}
function Kr(e, t) {
  return (t -= e = +e) ? function(n) {
    return (n - e) / t;
  } : Ho(isNaN(t) ? NaN : 0.5);
}
function Wo(e, t) {
  var n;
  return e > t && (n = e, e = t, t = n), function(r) {
    return Math.max(e, Math.min(t, r));
  };
}
function Vo(e, t, n) {
  var r = e[0], a = e[1], i = t[0], s = t[1];
  return a < r ? (r = Kr(a, r), i = n(s, i)) : (r = Kr(r, a), i = n(i, s)), function(o) {
    return i(r(o));
  };
}
function Yo(e, t, n) {
  var r = Math.min(e.length, t.length) - 1, a = new Array(r), i = new Array(r), s = -1;
  for (e[r] < e[0] && (e = e.slice().reverse(), t = t.slice().reverse()); ++s < r; )
    a[s] = Kr(e[s], e[s + 1]), i[s] = n(t[s], t[s + 1]);
  return function(o) {
    var u = Zs(e, o, 1, r) - 1;
    return i[u](a[u](o));
  };
}
function Xo(e, t) {
  return t.domain(e.domain()).range(e.range()).interpolate(e.interpolate()).clamp(e.clamp()).unknown(e.unknown());
}
function Go() {
  var e = $a, t = $a, n = rn, r, a, i, s = lt, o, u, f;
  function v() {
    var d = Math.min(e.length, t.length);
    return s !== lt && (s = Wo(e[0], e[d - 1])), o = d > 2 ? Yo : Vo, u = f = null, c;
  }
  function c(d) {
    return d == null || isNaN(d = +d) ? i : (u || (u = o(e.map(r), t, n)))(r(s(d)));
  }
  return c.invert = function(d) {
    return s(a((f || (f = o(t, e.map(r), nr)))(d)));
  }, c.domain = function(d) {
    return arguments.length ? (e = Array.from(d, jo), v()) : e.slice();
  }, c.range = function(d) {
    return arguments.length ? (t = Array.from(d), v()) : t.slice();
  }, c.rangeRound = function(d) {
    return t = Array.from(d), n = ga, v();
  }, c.clamp = function(d) {
    return arguments.length ? (s = d ? !0 : lt, v()) : s !== lt;
  }, c.interpolate = function(d) {
    return arguments.length ? (n = d, v()) : n;
  }, c.unknown = function(d) {
    return arguments.length ? (i = d, c) : i;
  }, function(d, g) {
    return r = d, a = g, v();
  };
}
function Uo() {
  return Go()(lt, lt);
}
function Ko(e) {
  return Math.abs(e = Math.round(e)) >= 1e21 ? e.toLocaleString("en").replace(/,/g, "") : e.toString(10);
}
function rr(e, t) {
  if ((n = (e = t ? e.toExponential(t - 1) : e.toExponential()).indexOf("e")) < 0) return null;
  var n, r = e.slice(0, n);
  return [
    r.length > 1 ? r[0] + r.slice(2) : r,
    +e.slice(n + 1)
  ];
}
function Kt(e) {
  return e = rr(Math.abs(e)), e ? e[1] : NaN;
}
function Zo(e, t) {
  return function(n, r) {
    for (var a = n.length, i = [], s = 0, o = e[0], u = 0; a > 0 && o > 0 && (u + o + 1 > r && (o = Math.max(1, r - u)), i.push(n.substring(a -= o, a + o)), !((u += o + 1) > r)); )
      o = e[s = (s + 1) % e.length];
    return i.reverse().join(t);
  };
}
function Qo(e) {
  return function(t) {
    return t.replace(/[0-9]/g, function(n) {
      return e[+n];
    });
  };
}
var Jo = /^(?:(.)?([<>=^]))?([+\-( ])?([$#])?(0)?(\d+)?(,)?(\.\d+)?(~)?([a-z%])?$/i;
function ar(e) {
  if (!(t = Jo.exec(e))) throw new Error("invalid format: " + e);
  var t;
  return new ha({
    fill: t[1],
    align: t[2],
    sign: t[3],
    symbol: t[4],
    zero: t[5],
    width: t[6],
    comma: t[7],
    precision: t[8] && t[8].slice(1),
    trim: t[9],
    type: t[10]
  });
}
ar.prototype = ha.prototype;
function ha(e) {
  this.fill = e.fill === void 0 ? " " : e.fill + "", this.align = e.align === void 0 ? ">" : e.align + "", this.sign = e.sign === void 0 ? "-" : e.sign + "", this.symbol = e.symbol === void 0 ? "" : e.symbol + "", this.zero = !!e.zero, this.width = e.width === void 0 ? void 0 : +e.width, this.comma = !!e.comma, this.precision = e.precision === void 0 ? void 0 : +e.precision, this.trim = !!e.trim, this.type = e.type === void 0 ? "" : e.type + "";
}
ha.prototype.toString = function() {
  return this.fill + this.align + this.sign + this.symbol + (this.zero ? "0" : "") + (this.width === void 0 ? "" : Math.max(1, this.width | 0)) + (this.comma ? "," : "") + (this.precision === void 0 ? "" : "." + Math.max(0, this.precision | 0)) + (this.trim ? "~" : "") + this.type;
};
function $o(e) {
  e: for (var t = e.length, n = 1, r = -1, a; n < t; ++n)
    switch (e[n]) {
      case ".":
        r = a = n;
        break;
      case "0":
        r === 0 && (r = n), a = n;
        break;
      default:
        if (!+e[n]) break e;
        r > 0 && (r = 0);
        break;
    }
  return r > 0 ? e.slice(0, r) + e.slice(a + 1) : e;
}
var tl;
function ef(e, t) {
  var n = rr(e, t);
  if (!n) return e + "";
  var r = n[0], a = n[1], i = a - (tl = Math.max(-8, Math.min(8, Math.floor(a / 3))) * 3) + 1, s = r.length;
  return i === s ? r : i > s ? r + new Array(i - s + 1).join("0") : i > 0 ? r.slice(0, i) + "." + r.slice(i) : "0." + new Array(1 - i).join("0") + rr(e, Math.max(0, t + i - 1))[0];
}
function ei(e, t) {
  var n = rr(e, t);
  if (!n) return e + "";
  var r = n[0], a = n[1];
  return a < 0 ? "0." + new Array(-a).join("0") + r : r.length > a + 1 ? r.slice(0, a + 1) + "." + r.slice(a + 1) : r + new Array(a - r.length + 2).join("0");
}
const ti = {
  "%": (e, t) => (e * 100).toFixed(t),
  b: (e) => Math.round(e).toString(2),
  c: (e) => e + "",
  d: Ko,
  e: (e, t) => e.toExponential(t),
  f: (e, t) => e.toFixed(t),
  g: (e, t) => e.toPrecision(t),
  o: (e) => Math.round(e).toString(8),
  p: (e, t) => ei(e * 100, t),
  r: ei,
  s: ef,
  X: (e) => Math.round(e).toString(16).toUpperCase(),
  x: (e) => Math.round(e).toString(16)
};
function ni(e) {
  return e;
}
var ri = Array.prototype.map, ai = ["y", "z", "a", "f", "p", "n", "µ", "m", "", "k", "M", "G", "T", "P", "E", "Z", "Y"];
function tf(e) {
  var t = e.grouping === void 0 || e.thousands === void 0 ? ni : Zo(ri.call(e.grouping, Number), e.thousands + ""), n = e.currency === void 0 ? "" : e.currency[0] + "", r = e.currency === void 0 ? "" : e.currency[1] + "", a = e.decimal === void 0 ? "." : e.decimal + "", i = e.numerals === void 0 ? ni : Qo(ri.call(e.numerals, String)), s = e.percent === void 0 ? "%" : e.percent + "", o = e.minus === void 0 ? "−" : e.minus + "", u = e.nan === void 0 ? "NaN" : e.nan + "";
  function f(c) {
    c = ar(c);
    var d = c.fill, g = c.align, h = c.sign, _ = c.symbol, w = c.zero, T = c.width, k = c.comma, p = c.precision, y = c.trim, S = c.type;
    S === "n" ? (k = !0, S = "g") : ti[S] || (p === void 0 && (p = 12), y = !0, S = "g"), (w || d === "0" && g === "=") && (w = !0, d = "0", g = "=");
    var C = _ === "$" ? n : _ === "#" && /[boxX]/.test(S) ? "0" + S.toLowerCase() : "", z = _ === "$" ? r : /[%p]/.test(S) ? s : "", H = ti[S], V = /[defgprs%]/.test(S);
    p = p === void 0 ? 6 : /[gprs]/.test(S) ? Math.max(1, Math.min(21, p)) : Math.max(0, Math.min(20, p));
    function J(E) {
      var R = C, L = z, q, A, N;
      if (S === "c")
        L = H(E) + L, E = "";
      else {
        E = +E;
        var Y = E < 0 || 1 / E < 0;
        if (E = isNaN(E) ? u : H(Math.abs(E), p), y && (E = $o(E)), Y && +E == 0 && h !== "+" && (Y = !1), R = (Y ? h === "(" ? h : o : h === "-" || h === "(" ? "" : h) + R, L = (S === "s" ? ai[8 + tl / 3] : "") + L + (Y && h === "(" ? ")" : ""), V) {
          for (q = -1, A = E.length; ++q < A; )
            if (N = E.charCodeAt(q), 48 > N || N > 57) {
              L = (N === 46 ? a + E.slice(q + 1) : E.slice(q)) + L, E = E.slice(0, q);
              break;
            }
        }
      }
      k && !w && (E = t(E, 1 / 0));
      var D = R.length + E.length + L.length, W = D < T ? new Array(T - D + 1).join(d) : "";
      switch (k && w && (E = t(W + E, W.length ? T - L.length : 1 / 0), W = ""), g) {
        case "<":
          E = R + E + L + W;
          break;
        case "=":
          E = R + W + E + L;
          break;
        case "^":
          E = W.slice(0, D = W.length >> 1) + R + E + L + W.slice(D);
          break;
        default:
          E = W + R + E + L;
          break;
      }
      return i(E);
    }
    return J.toString = function() {
      return c + "";
    }, J;
  }
  function v(c, d) {
    var g = f((c = ar(c), c.type = "f", c)), h = Math.max(-8, Math.min(8, Math.floor(Kt(d) / 3))) * 3, _ = Math.pow(10, -h), w = ai[8 + h / 3];
    return function(T) {
      return g(_ * T) + w;
    };
  }
  return {
    format: f,
    formatPrefix: v
  };
}
var Ln, Re, nl;
nf({
  thousands: ",",
  grouping: [3],
  currency: ["$", ""]
});
function nf(e) {
  return Ln = tf(e), Re = Ln.format, nl = Ln.formatPrefix, Ln;
}
function rf(e) {
  return Math.max(0, -Kt(Math.abs(e)));
}
function af(e, t) {
  return Math.max(0, Math.max(-8, Math.min(8, Math.floor(Kt(t) / 3))) * 3 - Kt(Math.abs(e)));
}
function lf(e, t) {
  return e = Math.abs(e), t = Math.abs(t) - e, Math.max(0, Kt(t) - Kt(e)) + 1;
}
function sf(e, t, n, r) {
  var a = io(e, t, n), i;
  switch (r = ar(r ?? ",f"), r.type) {
    case "s": {
      var s = Math.max(Math.abs(e), Math.abs(t));
      return r.precision == null && !isNaN(i = af(a, s)) && (r.precision = i), nl(r, s);
    }
    case "":
    case "e":
    case "g":
    case "p":
    case "r": {
      r.precision == null && !isNaN(i = lf(a, Math.max(Math.abs(e), Math.abs(t)))) && (r.precision = i - (r.type === "e"));
      break;
    }
    case "f":
    case "%": {
      r.precision == null && !isNaN(i = rf(a)) && (r.precision = i - (r.type === "%") * 2);
      break;
    }
  }
  return Re(r);
}
function ba(e) {
  var t = e.domain;
  return e.ticks = function(n) {
    var r = t();
    return ao(r[0], r[r.length - 1], n ?? 10);
  }, e.tickFormat = function(n, r) {
    var a = t();
    return sf(a[0], a[a.length - 1], n ?? 10, r);
  }, e.nice = function(n) {
    n == null && (n = 10);
    var r = t(), a = 0, i = r.length - 1, s = r[a], o = r[i], u, f, v = 10;
    for (o < s && (f = s, s = o, o = f, f = a, a = i, i = f); v-- > 0; ) {
      if (f = Gr(s, o, n), f === u)
        return r[a] = s, r[i] = o, t(r);
      if (f > 0)
        s = Math.floor(s / f) * f, o = Math.ceil(o / f) * f;
      else if (f < 0)
        s = Math.ceil(s * f) / f, o = Math.floor(o * f) / f;
      else
        break;
      u = f;
    }
    return e;
  }, e;
}
function Zt() {
  var e = Uo();
  return e.copy = function() {
    return Xo(e, Zt());
  }, ca.apply(e, arguments), ba(e);
}
function of() {
  var e = 0, t = 1, n, r, a, i, s = lt, o = !1, u;
  function f(c) {
    return c == null || isNaN(c = +c) ? u : s(a === 0 ? 0.5 : (c = (i(c) - n) * a, o ? Math.max(0, Math.min(1, c)) : c));
  }
  f.domain = function(c) {
    return arguments.length ? ([e, t] = c, n = i(e = +e), r = i(t = +t), a = n === r ? 0 : 1 / (r - n), f) : [e, t];
  }, f.clamp = function(c) {
    return arguments.length ? (o = !!c, f) : o;
  }, f.interpolator = function(c) {
    return arguments.length ? (s = c, f) : s;
  };
  function v(c) {
    return function(d) {
      var g, h;
      return arguments.length ? ([g, h] = d, s = c(g, h), f) : [s(0), s(1)];
    };
  }
  return f.range = v(rn), f.rangeRound = v(ga), f.unknown = function(c) {
    return arguments.length ? (u = c, f) : u;
  }, function(c) {
    return i = c, n = c(e), r = c(t), a = n === r ? 0 : 1 / (r - n), f;
  };
}
function rl(e, t) {
  return t.domain(e.domain()).interpolator(e.interpolator()).clamp(e.clamp()).unknown(e.unknown());
}
function Ft() {
  var e = ba(of()(lt));
  return e.copy = function() {
    return rl(e, Ft());
  }, Zi.apply(e, arguments);
}
function ff() {
  var e = 0, t = 0.5, n = 1, r = 1, a, i, s, o, u, f = lt, v, c = !1, d;
  function g(_) {
    return isNaN(_ = +_) ? d : (_ = 0.5 + ((_ = +v(_)) - i) * (r * _ < r * i ? o : u), f(c ? Math.max(0, Math.min(1, _)) : _));
  }
  g.domain = function(_) {
    return arguments.length ? ([e, t, n] = _, a = v(e = +e), i = v(t = +t), s = v(n = +n), o = a === i ? 0 : 0.5 / (i - a), u = i === s ? 0 : 0.5 / (s - i), r = i < a ? -1 : 1, g) : [e, t, n];
  }, g.clamp = function(_) {
    return arguments.length ? (c = !!_, g) : c;
  }, g.interpolator = function(_) {
    return arguments.length ? (f = _, g) : f;
  };
  function h(_) {
    return function(w) {
      var T, k, p;
      return arguments.length ? ([T, k, p] = w, f = Bo(_, [T, k, p]), g) : [f(0), f(0.5), f(1)];
    };
  }
  return g.range = h(rn), g.rangeRound = h(ga), g.unknown = function(_) {
    return arguments.length ? (d = _, g) : d;
  }, function(_) {
    return v = _, a = _(e), i = _(t), s = _(n), o = a === i ? 0 : 0.5 / (i - a), u = i === s ? 0 : 0.5 / (s - i), r = i < a ? -1 : 1, g;
  };
}
function _a() {
  var e = ba(ff()(lt));
  return e.copy = function() {
    return rl(e, _a());
  }, Zi.apply(e, arguments);
}
function uf(e, t, n) {
  let r = 0;
  for (; r <= e; ) {
    const a = Math.floor((r + e) / 2), i = t(a);
    if (i === n)
      return a;
    i < n ? r = a + 1 : e = a - 1;
  }
  return e;
}
function ii(e, t, n) {
  const r = e.measureText(t).width, a = "…", i = e.measureText(a).width;
  if (r <= n || r <= i)
    return t;
  const s = uf(
    t.length - 1,
    (o) => e.measureText(t.substring(0, o)).width,
    n - i
  );
  return t.substring(0, s) + a;
}
function al(e, t, n, r, a, i, s, o) {
  const u = Math.min(...n.range()), f = Math.max(...n.range()), v = (u + f) / 2, c = e === "left", d = e === "right", g = e === "top";
  if (c || d) {
    const h = c ? -r : i;
    if (t === "top") {
      const _ = u - a, w = 0.71 * o;
      return {
        textAlign: c ? "start" : "end",
        x: h,
        y: _ + w,
        rotate: 0
      };
    } else {
      if (t === "bottom")
        return {
          textAlign: c ? "start" : "end",
          x: h,
          y: f + s,
          rotate: 0
        };
      {
        const _ = c ? 1 : -1, w = h + _ * o / 2, T = v, k = _ * 0.71 * o;
        return {
          textAlign: "center",
          x: w + k,
          y: T,
          rotate: c ? -90 : 90
        };
      }
    }
  } else {
    const h = g ? -a + o / 2 : s - o / 2, _ = g ? o * 0.71 : 0;
    return t === "left" ? {
      textAlign: "start",
      x: u - r,
      y: h + _,
      rotate: 0
    } : t === "right" ? {
      textAlign: "end",
      x: f + i,
      y: h + _,
      rotate: 0
    } : {
      textAlign: "center",
      x: v,
      y: h + _,
      rotate: 0
    };
  }
}
function li(e, t) {
  return e === "left" ? "end" : e === "right" ? "start" : t === 0 ? "center" : t > 0 && e === "top" ? "end" : t < 0 && e === "top" || t > 0 && e === "bottom" ? "start" : "end";
}
const Rr = {
  start: "start",
  center: "middle",
  end: "end"
};
function si(e, t, n, {
  translateX: r = 0,
  translateY: a = 0,
  marginLeft: i = 0,
  marginTop: s = 0,
  marginRight: o = 0,
  marginBottom: u = 0,
  tickLineSize: f = 6,
  tickLabelFontSize: v = 10,
  tickLabelFontFamily: c = "ui-sans-serif, system-ui, sans-serif",
  tickLabelAngle: d = 0,
  tickPadding: g = 3,
  tickFormat: h,
  numTicks: _,
  tickValues: w,
  showTickMarks: T = !0,
  showTickLabels: k = !0,
  maxTickLabelSpace: p,
  tickLineColor: y = "black",
  tickLabelColor: S = "black",
  showDomain: C = !1,
  domainColor: z = "black",
  title: H = "",
  titleFontSize: V = 12,
  titleFontFamily: J = "ui-sans-serif, system-ui, sans-serif",
  titleFontWeight: E = 400,
  titleAnchor: R = "center",
  titleOffsetX: L = 0,
  titleOffsetY: q = 0,
  titleColor: A = "black"
} = {}) {
  const N = t === "top" || t === "left" ? -1 : 1, Y = Math.max(f, 0) + g, D = n.bandwidth ? n.bandwidth() / 2 : 0, W = al(
    t,
    R,
    n,
    i,
    s,
    o,
    u,
    V
  ), $ = w ?? (n.ticks ? n.ticks(_) : n.domain()), j = h ?? (n.tickFormat ? n.tickFormat(_) : (B) => String(B).toString());
  e.save(), e.translate(r, a), e.font = `${v}px ${c}`, e.globalAlpha = 1, e.fillStyle = S, e.strokeStyle = y, t === "left" || t === "right" ? ($.forEach((B) => {
    const O = (n(B) ?? 0) + D;
    if (T && (e.beginPath(), e.moveTo(f * N, O), e.lineTo(0, O), e.stroke()), k) {
      e.save(), e.translate(Y * N, O), e.rotate(d * Math.PI / 180), e.textBaseline = "middle", e.textAlign = t === "left" ? "end" : "start";
      const X = p ? ii(e, j(B), p) : j(B);
      e.fillText(X, 0, 0), e.restore();
    }
  }), e.strokeStyle = z, e.lineWidth = 1, C && (e.beginPath(), e.moveTo(0, n.range()[0]), e.lineTo(0, n.range()[1]), e.stroke())) : ($.forEach((B) => {
    const O = (n(B) ?? 0) + D;
    if (T && (e.beginPath(), e.moveTo(O, f * N), e.lineTo(O, 0), e.stroke()), k) {
      e.save(), e.translate(O, Y * N), e.rotate(d * Math.PI / 180), e.textBaseline = t === "top" ? "bottom" : "top", e.textAlign = "center";
      const X = p ? ii(e, j(B), p) : j(B);
      e.fillText(X, 0, 0), e.restore();
    }
  }), e.strokeStyle = z, e.lineWidth = 1, C && (e.beginPath(), e.moveTo(n.range()[0], 0), e.lineTo(n.range()[1], 0), e.stroke())), H && (e.fillStyle = A, e.textAlign = W.textAlign, e.textBaseline = "alphabetic", e.font = `${E} ${V}px ${J}`, e.translate(W.x, W.y), e.rotate(W.rotate * Math.PI / 180), e.fillText(H, L, q)), e.restore();
}
var cf = /* @__PURE__ */ we("<text><tspan></tspan> <title> </title></text>");
function oi(e, t) {
  me(t, !0);
  let n = F(t, "angle", 3, 0), r = F(t, "fontSize", 3, 10), a = F(t, "fontFamily", 3, "ui-sans-serif, system-ui, sans-serif"), i = F(t, "fontColor", 3, "black"), s = F(t, "fontWeight", 3, 400), o = F(t, "dominantBaseline", 3, "auto"), u = F(t, "textAnchor", 3, "start"), f = /* @__PURE__ */ se(void 0);
  function v(_, w, T) {
    T.textContent = _;
    let k = _;
    for (; k.length > 0 && T.getComputedTextLength() > w; )
      k = k.slice(0, -1), T.textContent = k + "…";
  }
  Dr(() => {
    l(f) && v(t.label, t.width, l(f));
  });
  var c = cf(), d = b(c);
  Zn(d, (_) => ee(f, _), () => l(f));
  var g = m(d, 2), h = b(g);
  ne(() => {
    M(c, "fill", i()), M(c, "font-size", r()), M(c, "font-family", a()), M(c, "font-weight", s()), M(c, "transform", `translate(${t.x ?? ""} ${t.y ?? ""}) rotate(${n() ?? ""})`), M(d, "dominant-baseline", o()), M(d, "text-anchor", u()), de(h, t.label);
  }), I(e, c), xe();
}
var df = /* @__PURE__ */ we("<line></line>"), vf = /* @__PURE__ */ we("<text> </text>"), gf = /* @__PURE__ */ we("<g><!><!></g>"), hf = /* @__PURE__ */ we("<line></line>"), bf = /* @__PURE__ */ we("<g></g><!>", 1), _f = /* @__PURE__ */ we("<line></line>"), mf = /* @__PURE__ */ we("<text> </text>"), xf = /* @__PURE__ */ we("<g><!><!></g>"), pf = /* @__PURE__ */ we("<line></line>"), wf = /* @__PURE__ */ we("<g></g><!>", 1), yf = /* @__PURE__ */ we("<text> </text>"), kf = /* @__PURE__ */ we("<g><!><!></g>");
function Qt(e, t) {
  me(t, !0);
  let n = F(t, "translateX", 3, 0), r = F(t, "translateY", 3, 0), a = F(t, "marginLeft", 3, 0), i = F(t, "marginTop", 3, 0), s = F(t, "marginRight", 3, 0), o = F(t, "marginBottom", 3, 0), u = F(t, "tickLineSize", 3, 6), f = F(t, "tickLabelFontSize", 3, 10), v = F(t, "tickLabelFontFamily", 3, "ui-sans-serif, system-ui, sans-serif"), c = F(t, "tickLabelAngle", 3, 0), d = F(t, "tickPadding", 3, 3), g = F(t, "showTickMarks", 3, !0), h = F(t, "showTickLabels", 3, !0), _ = F(t, "tickLineColor", 3, "black"), w = F(t, "tickLabelColor", 3, "black"), T = F(t, "showDomain", 3, !1), k = F(t, "domainColor", 3, "black"), p = F(t, "title", 3, ""), y = F(t, "titleFontSize", 3, 12), S = F(t, "titleFontFamily", 3, "ui-sans-serif, system-ui, sans-serif"), C = F(t, "titleFontWeight", 3, 400), z = F(t, "titleAnchor", 3, "center"), H = F(t, "titleOffsetX", 3, 0), V = F(t, "titleOffsetY", 3, 0), J = F(t, "titleColor", 3, "black");
  const E = /* @__PURE__ */ x(() => t.orientation === "top" || t.orientation === "left" ? -1 : 1), R = /* @__PURE__ */ x(() => Math.max(u(), 0) + d()), L = /* @__PURE__ */ x(() => t.scale.bandwidth ? t.scale.bandwidth() / 2 : 0), q = /* @__PURE__ */ x(() => al(t.orientation, z(), t.scale, a(), i(), s(), o(), y()));
  let A = /* @__PURE__ */ x(() => t.tickValues ?? (t.scale.ticks ? t.scale.ticks(t.numTicks) : t.scale.domain())), N = /* @__PURE__ */ x(() => t.tickFormat ?? (t.scale.tickFormat ? t.scale.tickFormat(t.numTicks) : (O) => String(O).toString()));
  var Y = kf(), D = b(Y);
  {
    var W = (O) => {
      var X = bf(), Q = Ee(X);
      ke(Q, 21, () => l(A), ye, (ie, K) => {
        var he = gf();
        const _e = /* @__PURE__ */ x(() => (t.scale(l(K)) ?? 0) + l(L));
        var pe = b(he);
        {
          var Le = (G) => {
            var Z = df();
            M(Z, "y1", 0), M(Z, "x2", 0), M(Z, "y2", 0), ne(() => {
              M(Z, "x1", u() * l(E)), M(Z, "stroke", _());
            }), I(G, Z);
          };
          le(pe, (G) => {
            g() && G(Le);
          });
        }
        var je = m(pe);
        {
          var P = (G) => {
            var Z = qt();
            const fe = /* @__PURE__ */ x(() => Rr[li(t.orientation, c())]);
            var Me = Ee(Z);
            {
              var Te = (ue) => {
                const ve = /* @__PURE__ */ x(() => l(N)(l(K))), Ue = /* @__PURE__ */ x(() => l(R) * l(E));
                oi(ue, {
                  get label() {
                    return l(ve);
                  },
                  get width() {
                    return t.maxTickLabelSpace;
                  },
                  get x() {
                    return l(Ue);
                  },
                  y: 0,
                  dominantBaseline: "middle",
                  get textAnchor() {
                    return l(fe);
                  },
                  get fontSize() {
                    return f();
                  },
                  get fontColor() {
                    return w();
                  },
                  get fontFamily() {
                    return v();
                  },
                  get angle() {
                    return c();
                  }
                });
              }, Ne = (ue) => {
                var ve = vf();
                M(ve, "dominant-baseline", "middle");
                var Ue = b(ve);
                ne(
                  (Ae) => {
                    M(ve, "text-anchor", l(fe)), M(ve, "transform", `translate(${l(R) * l(E)} 0) rotate(${c() ?? ""})`), M(ve, "fill", w()), M(ve, "font-size", f()), M(ve, "font-family", v()), de(Ue, Ae);
                  },
                  [() => l(N)(l(K))]
                ), I(ue, ve);
              };
              le(Me, (ue) => {
                t.maxTickLabelSpace ? ue(Te) : ue(Ne, !1);
              });
            }
            I(G, Z);
          };
          le(je, (G) => {
            h() && G(P);
          });
        }
        ne(() => M(he, "transform", `translate(0,${l(_e) ?? ""})`)), I(ie, he);
      });
      var U = m(Q);
      {
        var re = (ie) => {
          var K = hf();
          M(K, "x1", 0), M(K, "x2", 0), M(K, "stroke-width", 1), ne(
            (he, _e) => {
              M(K, "y1", he), M(K, "y2", _e), M(K, "stroke", k());
            },
            [
              () => t.scale.range()[0],
              () => t.scale.range()[1]
            ]
          ), I(ie, K);
        };
        le(U, (ie) => {
          T() && ie(re);
        });
      }
      I(O, X);
    }, $ = (O) => {
      var X = wf(), Q = Ee(X);
      ke(Q, 21, () => l(A), ye, (ie, K) => {
        var he = xf();
        const _e = /* @__PURE__ */ x(() => (t.scale(l(K)) ?? 0) + l(L));
        var pe = b(he);
        {
          var Le = (G) => {
            var Z = _f();
            M(Z, "x1", 0), M(Z, "x2", 0), M(Z, "y2", 0), ne(() => {
              M(Z, "y1", u() * l(E)), M(Z, "stroke", _());
            }), I(G, Z);
          };
          le(pe, (G) => {
            g() && G(Le);
          });
        }
        var je = m(pe);
        {
          var P = (G) => {
            var Z = qt();
            const fe = /* @__PURE__ */ x(() => Rr[li(t.orientation, c())]);
            var Me = Ee(Z);
            {
              var Te = (ue) => {
                const ve = /* @__PURE__ */ x(() => l(N)(l(K))), Ue = /* @__PURE__ */ x(() => l(R) * l(E)), Ae = /* @__PURE__ */ x(() => t.orientation === "top" ? "text-top" : "hanging");
                oi(ue, {
                  get label() {
                    return l(ve);
                  },
                  get width() {
                    return t.maxTickLabelSpace;
                  },
                  x: 0,
                  get y() {
                    return l(Ue);
                  },
                  get dominantBaseline() {
                    return l(Ae);
                  },
                  get textAnchor() {
                    return l(fe);
                  },
                  get fontSize() {
                    return f();
                  },
                  get fontFamily() {
                    return v();
                  },
                  get fontColor() {
                    return w();
                  },
                  get angle() {
                    return c();
                  }
                });
              }, Ne = (ue) => {
                var ve = mf(), Ue = b(ve);
                ne(
                  (Ae) => {
                    M(ve, "dominant-baseline", t.orientation === "top" ? "text-top" : "hanging"), M(ve, "text-anchor", l(fe)), M(ve, "transform", `translate(0 ${l(R) * l(E)}) rotate(${c() ?? ""})`), M(ve, "font-size", f()), M(ve, "font-family", v()), M(ve, "fill", w()), de(Ue, Ae);
                  },
                  [() => l(N)(l(K))]
                ), I(ue, ve);
              };
              le(Me, (ue) => {
                t.maxTickLabelSpace ? ue(Te) : ue(Ne, !1);
              });
            }
            I(G, Z);
          };
          le(je, (G) => {
            h() && G(P);
          });
        }
        ne(() => M(he, "transform", `translate(${l(_e) ?? ""},0)`)), I(ie, he);
      });
      var U = m(Q);
      {
        var re = (ie) => {
          var K = pf();
          M(K, "y1", 0), M(K, "y2", 0), M(K, "stroke-width", 1), ne(
            (he, _e) => {
              M(K, "x1", he), M(K, "x2", _e), M(K, "stroke", k());
            },
            [
              () => t.scale.range()[0],
              () => t.scale.range()[1]
            ]
          ), I(ie, K);
        };
        le(U, (ie) => {
          T() && ie(re);
        });
      }
      I(O, X);
    };
    le(D, (O) => {
      t.orientation === "left" || t.orientation == "right" ? O(W) : O($, !1);
    });
  }
  var j = m(D);
  {
    var B = (O) => {
      var X = yf(), Q = b(X);
      ne(() => {
        M(X, "fill", J()), M(X, "font-size", y()), M(X, "font-family", S()), M(X, "font-weight", C()), M(X, "text-anchor", Rr[l(q).textAlign]), M(X, "transform", `translate(${l(q).x ?? ""} ${l(q).y ?? ""}) rotate(${l(q).rotate ?? ""}) translate(${H() ?? ""} ${V() ?? ""})`), de(Q, p());
      }), I(O, X);
    };
    le(j, (O) => {
      p() && O(B);
    });
  }
  ne(() => M(Y, "transform", `translate(${n() ?? ""},${r() ?? ""})`)), I(e, Y), xe();
}
function Tt(e) {
  for (var t = e.length / 6 | 0, n = new Array(t), r = 0; r < t; ) n[r] = "#" + e.slice(r * 6, ++r * 6);
  return n;
}
const pr = (e) => Fo(e[e.length - 1]);
var Mf = new Array(3).concat(
  "af8dc3f7f7f77fbf7b",
  "7b3294c2a5cfa6dba0008837",
  "7b3294c2a5cff7f7f7a6dba0008837",
  "762a83af8dc3e7d4e8d9f0d37fbf7b1b7837",
  "762a83af8dc3e7d4e8f7f7f7d9f0d37fbf7b1b7837",
  "762a839970abc2a5cfe7d4e8d9f0d3a6dba05aae611b7837",
  "762a839970abc2a5cfe7d4e8f7f7f7d9f0d3a6dba05aae611b7837",
  "40004b762a839970abc2a5cfe7d4e8d9f0d3a6dba05aae611b783700441b",
  "40004b762a839970abc2a5cfe7d4e8f7f7f7d9f0d3a6dba05aae611b783700441b"
).map(Tt);
const Tf = pr(Mf);
var Af = new Array(3).concat(
  "e9a3c9f7f7f7a1d76a",
  "d01c8bf1b6dab8e1864dac26",
  "d01c8bf1b6daf7f7f7b8e1864dac26",
  "c51b7de9a3c9fde0efe6f5d0a1d76a4d9221",
  "c51b7de9a3c9fde0eff7f7f7e6f5d0a1d76a4d9221",
  "c51b7dde77aef1b6dafde0efe6f5d0b8e1867fbc414d9221",
  "c51b7dde77aef1b6dafde0eff7f7f7e6f5d0b8e1867fbc414d9221",
  "8e0152c51b7dde77aef1b6dafde0efe6f5d0b8e1867fbc414d9221276419",
  "8e0152c51b7dde77aef1b6dafde0eff7f7f7e6f5d0b8e1867fbc414d9221276419"
).map(Tt);
const Sf = pr(Af);
var Ef = new Array(3).concat(
  "deebf79ecae13182bd",
  "eff3ffbdd7e76baed62171b5",
  "eff3ffbdd7e76baed63182bd08519c",
  "eff3ffc6dbef9ecae16baed63182bd08519c",
  "eff3ffc6dbef9ecae16baed64292c62171b5084594",
  "f7fbffdeebf7c6dbef9ecae16baed64292c62171b5084594",
  "f7fbffdeebf7c6dbef9ecae16baed64292c62171b508519c08306b"
).map(Tt);
const il = pr(Ef);
var Lf = new Array(3).concat(
  "fee6cefdae6be6550d",
  "feeddefdbe85fd8d3cd94701",
  "feeddefdbe85fd8d3ce6550da63603",
  "feeddefdd0a2fdae6bfd8d3ce6550da63603",
  "feeddefdd0a2fdae6bfd8d3cf16913d948018c2d04",
  "fff5ebfee6cefdd0a2fdae6bfd8d3cf16913d948018c2d04",
  "fff5ebfee6cefdd0a2fdae6bfd8d3cf16913d94801a636037f2704"
).map(Tt);
const Nf = pr(Lf);
function wr(e) {
  var t = e.length;
  return function(n) {
    return e[Math.max(0, Math.min(t - 1, Math.floor(n * t)))];
  };
}
wr(Tt("44015444025645045745055946075a46085c460a5d460b5e470d60470e6147106347116447136548146748166848176948186a481a6c481b6d481c6e481d6f481f70482071482173482374482475482576482677482878482979472a7a472c7a472d7b472e7c472f7d46307e46327e46337f463480453581453781453882443983443a83443b84433d84433e85423f854240864241864142874144874045884046883f47883f48893e49893e4a893e4c8a3d4d8a3d4e8a3c4f8a3c508b3b518b3b528b3a538b3a548c39558c39568c38588c38598c375a8c375b8d365c8d365d8d355e8d355f8d34608d34618d33628d33638d32648e32658e31668e31678e31688e30698e306a8e2f6b8e2f6c8e2e6d8e2e6e8e2e6f8e2d708e2d718e2c718e2c728e2c738e2b748e2b758e2a768e2a778e2a788e29798e297a8e297b8e287c8e287d8e277e8e277f8e27808e26818e26828e26828e25838e25848e25858e24868e24878e23888e23898e238a8d228b8d228c8d228d8d218e8d218f8d21908d21918c20928c20928c20938c1f948c1f958b1f968b1f978b1f988b1f998a1f9a8a1e9b8a1e9c891e9d891f9e891f9f881fa0881fa1881fa1871fa28720a38620a48621a58521a68522a78522a88423a98324aa8325ab8225ac8226ad8127ad8128ae8029af7f2ab07f2cb17e2db27d2eb37c2fb47c31b57b32b67a34b67935b77937b87838b9773aba763bbb753dbc743fbc7340bd7242be7144bf7046c06f48c16e4ac16d4cc26c4ec36b50c46a52c56954c56856c66758c7655ac8645cc8635ec96260ca6063cb5f65cb5e67cc5c69cd5b6ccd5a6ece5870cf5773d05675d05477d1537ad1517cd2507fd34e81d34d84d44b86d54989d5488bd6468ed64590d74393d74195d84098d83e9bd93c9dd93ba0da39a2da37a5db36a8db34aadc32addc30b0dd2fb2dd2db5de2bb8de29bade28bddf26c0df25c2df23c5e021c8e020cae11fcde11dd0e11cd2e21bd5e21ad8e219dae319dde318dfe318e2e418e5e419e7e419eae51aece51befe51cf1e51df4e61ef6e620f8e621fbe723fde725"));
wr(Tt("00000401000501010601010802010902020b02020d03030f03031204041405041606051806051a07061c08071e0907200a08220b09240c09260d0a290e0b2b100b2d110c2f120d31130d34140e36150e38160f3b180f3d19103f1a10421c10441d11471e114920114b21114e22115024125325125527125829115a2a115c2c115f2d11612f116331116533106734106936106b38106c390f6e3b0f703d0f713f0f72400f74420f75440f764510774710784910784a10794c117a4e117b4f127b51127c52137c54137d56147d57157e59157e5a167e5c167f5d177f5f187f601880621980641a80651a80671b80681c816a1c816b1d816d1d816e1e81701f81721f817320817521817621817822817922827b23827c23827e24828025828125818326818426818627818827818928818b29818c29818e2a81902a81912b81932b80942c80962c80982d80992d809b2e7f9c2e7f9e2f7fa02f7fa1307ea3307ea5317ea6317da8327daa337dab337cad347cae347bb0357bb2357bb3367ab5367ab73779b83779ba3878bc3978bd3977bf3a77c03a76c23b75c43c75c53c74c73d73c83e73ca3e72cc3f71cd4071cf4070d0416fd2426fd3436ed5446dd6456cd8456cd9466bdb476adc4869de4968df4a68e04c67e24d66e34e65e44f64e55064e75263e85362e95462ea5661eb5760ec5860ed5a5fee5b5eef5d5ef05f5ef1605df2625df2645cf3655cf4675cf4695cf56b5cf66c5cf66e5cf7705cf7725cf8745cf8765cf9785df9795df97b5dfa7d5efa7f5efa815ffb835ffb8560fb8761fc8961fc8a62fc8c63fc8e64fc9065fd9266fd9467fd9668fd9869fd9a6afd9b6bfe9d6cfe9f6dfea16efea36ffea571fea772fea973feaa74feac76feae77feb078feb27afeb47bfeb67cfeb77efeb97ffebb81febd82febf84fec185fec287fec488fec68afec88cfeca8dfecc8ffecd90fecf92fed194fed395fed597fed799fed89afdda9cfddc9efddea0fde0a1fde2a3fde3a5fde5a7fde7a9fde9aafdebacfcecaefceeb0fcf0b2fcf2b4fcf4b6fcf6b8fcf7b9fcf9bbfcfbbdfcfdbf"));
wr(Tt("00000401000501010601010802010a02020c02020e03021004031204031405041706041907051b08051d09061f0a07220b07240c08260d08290e092b10092d110a30120a32140b34150b37160b39180c3c190c3e1b0c411c0c431e0c451f0c48210c4a230c4c240c4f260c51280b53290b552b0b572d0b592f0a5b310a5c320a5e340a5f3609613809623909633b09643d09653e0966400a67420a68440a68450a69470b6a490b6a4a0c6b4c0c6b4d0d6c4f0d6c510e6c520e6d540f6d550f6d57106e59106e5a116e5c126e5d126e5f136e61136e62146e64156e65156e67166e69166e6a176e6c186e6d186e6f196e71196e721a6e741a6e751b6e771c6d781c6d7a1d6d7c1d6d7d1e6d7f1e6c801f6c82206c84206b85216b87216b88226a8a226a8c23698d23698f24699025689225689326679526679727669827669a28659b29649d29649f2a63a02a63a22b62a32c61a52c60a62d60a82e5fa92e5eab2f5ead305dae305cb0315bb1325ab3325ab43359b63458b73557b93556ba3655bc3754bd3853bf3952c03a51c13a50c33b4fc43c4ec63d4dc73e4cc83f4bca404acb4149cc4248ce4347cf4446d04545d24644d34743d44842d54a41d74b3fd84c3ed94d3dda4e3cdb503bdd513ade5238df5337e05536e15635e25734e35933e45a31e55c30e65d2fe75e2ee8602de9612bea632aeb6429eb6628ec6726ed6925ee6a24ef6c23ef6e21f06f20f1711ff1731df2741cf3761bf37819f47918f57b17f57d15f67e14f68013f78212f78410f8850ff8870ef8890cf98b0bf98c0af98e09fa9008fa9207fa9407fb9606fb9706fb9906fb9b06fb9d07fc9f07fca108fca309fca50afca60cfca80dfcaa0ffcac11fcae12fcb014fcb216fcb418fbb61afbb81dfbba1ffbbc21fbbe23fac026fac228fac42afac62df9c72ff9c932f9cb35f8cd37f8cf3af7d13df7d340f6d543f6d746f5d949f5db4cf4dd4ff4df53f4e156f3e35af3e55df2e661f2e865f2ea69f1ec6df1ed71f1ef75f1f179f2f27df2f482f3f586f3f68af4f88ef5f992f6fa96f8fb9af9fc9dfafda1fcffa4"));
var Zr = wr(Tt("0d088710078813078916078a19068c1b068d1d068e20068f2206902406912605912805922a05932c05942e05952f059631059733059735049837049938049a3a049a3c049b3e049c3f049c41049d43039e44039e46039f48039f4903a04b03a14c02a14e02a25002a25102a35302a35502a45601a45801a45901a55b01a55c01a65e01a66001a66100a76300a76400a76600a76700a86900a86a00a86c00a86e00a86f00a87100a87201a87401a87501a87701a87801a87a02a87b02a87d03a87e03a88004a88104a78305a78405a78606a68707a68808a68a09a58b0aa58d0ba58e0ca48f0da4910ea3920fa39410a29511a19613a19814a099159f9a169f9c179e9d189d9e199da01a9ca11b9ba21d9aa31e9aa51f99a62098a72197a82296aa2395ab2494ac2694ad2793ae2892b02991b12a90b22b8fb32c8eb42e8db52f8cb6308bb7318ab83289ba3388bb3488bc3587bd3786be3885bf3984c03a83c13b82c23c81c33d80c43e7fc5407ec6417dc7427cc8437bc9447aca457acb4679cc4778cc4977cd4a76ce4b75cf4c74d04d73d14e72d24f71d35171d45270d5536fd5546ed6556dd7566cd8576bd9586ada5a6ada5b69db5c68dc5d67dd5e66de5f65de6164df6263e06363e16462e26561e26660e3685fe4695ee56a5de56b5de66c5ce76e5be76f5ae87059e97158e97257ea7457eb7556eb7655ec7754ed7953ed7a52ee7b51ef7c51ef7e50f07f4ff0804ef1814df1834cf2844bf3854bf3874af48849f48948f58b47f58c46f68d45f68f44f79044f79143f79342f89441f89540f9973ff9983ef99a3efa9b3dfa9c3cfa9e3bfb9f3afba139fba238fca338fca537fca636fca835fca934fdab33fdac33fdae32fdaf31fdb130fdb22ffdb42ffdb52efeb72dfeb82cfeba2cfebb2bfebd2afebe2afec029fdc229fdc328fdc527fdc627fdc827fdca26fdcb26fccd25fcce25fcd025fcd225fbd324fbd524fbd724fad824fada24f9dc24f9dd25f8df25f8e125f7e225f7e425f6e626f6e826f5e926f5eb27f4ed27f3ee27f3f027f2f227f1f426f1f525f0f724f0f921"));
function Ff(e, t, n, r) {
  const a = window.devicePixelRatio || 1;
  e.width = n * a, e.height = r * a, e.style.width = `${n}px`, e.style.height = `${r}px`, t.scale(a, a);
}
function ma(e, t, n) {
  const r = Math.min(e / n, t);
  return {
    width: n * r,
    height: r
  };
}
function ll(e, t, n, r, a, i, s) {
  const o = e - a - s, u = t - r - i, f = ma(o, u, n);
  return {
    width: f.width + a + s,
    height: f.height + r + i
  };
}
function Qr(e) {
  return e >= 1e-3 && e <= 1 || e >= -1 && e <= 1e-3 ? Re(".3~f")(e) : Re("~s")(e);
}
function ir(e) {
  return e < 1e-5 ? Re(".1~p")(e) : e < 1e-3 ? Re(".2~p")(e) : Re(".3~p")(e);
}
const fi = Re(".3~f"), gt = Re(".2~f"), ui = Re(".2~f"), Cf = Re(".3~f"), Jt = Re(".2~%"), ci = (e) => Re(".2~f")(e * 100), jt = Re(",d"), di = Re(".3~s"), sl = [
  {
    key: "Instance count",
    value: (e, t, n) => jt(n)
  },
  {
    key: "Activation value",
    value: (e, t, n) => `${gt(e)} to ${gt(t)}`
  }
];
var qf = /* @__PURE__ */ te("<canvas></canvas>");
function _n(e, t) {
  me(t, !0);
  let n = F(t, "orientation", 3, "horizontal"), r = F(t, "marginTop", 3, 10), a = F(t, "marginRight", 3, 10), i = F(t, "marginBottom", 3, 10), s = F(t, "marginLeft", 3, 10), o = F(t, "title", 3, ""), u = F(t, "tickLabelFontSize", 3, 10), f = F(t, "titleFontSize", 3, 12), v = /* @__PURE__ */ se(null), c = /* @__PURE__ */ x(() => l(v) ? l(v).getContext("2d", { alpha: !1 }) : null);
  function d(_, w, T, k, p, y, S, C) {
    const z = Zt().domain([
      w.domain()[0],
      w.domain()[w.domain().length - 1]
    ]).range([C, T - y]), H = z.range()[1] - z.range()[0], V = k - p - S, J = w.domain().length, E = t.tickValues ?? z.ticks(Math.max(Math.min(H / 50, 10), J));
    _.fillStyle = "white", _.fillRect(0, 0, T, k);
    for (let R = 0; R < H; R++)
      _.fillStyle = w.interpolator()(R / H), _.fillRect(R + C, p, 1, V);
    si(_, "bottom", z, {
      translateY: k - S,
      tickValues: E,
      tickFormat: t.tickFormat,
      title: o(),
      titleAnchor: "left",
      titleOffsetX: C,
      titleOffsetY: -S - V,
      marginTop: p,
      marginRight: y,
      marginBottom: S,
      marginLeft: C,
      tickLabelFontSize: u(),
      titleFontSize: f(),
      numTicks: t.numTicks
    });
  }
  function g(_, w, T, k, p, y, S, C) {
    const z = Zt().domain([
      w.domain()[0],
      w.domain()[w.domain().length - 1]
    ]).range([k - S, p]), H = T - C - y, V = z.range()[0] - z.range()[1];
    _.fillStyle = "white", _.fillRect(0, 0, T, k);
    for (let J = 0; J < V; J++)
      _.fillStyle = w.interpolator()(1 - J / V), _.fillRect(C, J + p, H, 1);
    si(_, "right", z, {
      translateX: T - y,
      tickValues: t.tickValues,
      tickFormat: t.tickFormat,
      title: o(),
      marginTop: p,
      marginRight: y,
      marginBottom: S,
      marginLeft: C,
      tickLabelFontSize: u(),
      titleFontSize: f(),
      numTicks: t.numTicks
    });
  }
  Dr(() => {
    l(v) && l(c) && Ff(l(v), l(c), t.width, t.height);
  }), Dr(() => {
    l(c) && (n() === "horizontal" ? d(l(c), t.color, t.width, t.height, r(), a(), i(), s()) : g(l(c), t.color, t.width, t.height, r(), a(), i(), s()));
  });
  var h = qf();
  Zn(h, (_) => ee(v, _), () => l(v)), I(e, h), xe();
}
var Pf = /* @__PURE__ */ te('<div class="sae-tooltip svelte-medmur"><!></div>');
function yr(e, t) {
  me(t, !0);
  function n(g, h, _, w) {
    return _.top - g < h.top ? _.bottom - h.top + w : _.top - h.top - g - w;
  }
  function r(g, h, _, w) {
    const T = g / 2, k = (_.left + _.right) / 2;
    return k - T < h.left ? _.right - h.left + w : k + T > h.right ? _.left - h.left - g - w : _.left - h.left + _.width / 2 - T;
  }
  const a = 4;
  let i = /* @__PURE__ */ se(0), s = /* @__PURE__ */ se(0);
  const o = /* @__PURE__ */ x(() => t.anchor.getBoundingClientRect()), u = /* @__PURE__ */ x(() => fa.value.getBoundingClientRect());
  let f = /* @__PURE__ */ x(() => n(l(s), l(u), l(o), a)), v = /* @__PURE__ */ x(() => r(l(i), l(u), l(o), a));
  var c = Pf(), d = b(c);
  jr(d, () => t.children), ne(() => Be(c, `left: ${l(v) ?? ""}px; top: ${l(f) ?? ""}px;`)), Qe(c, "offsetWidth", (g) => ee(i, g)), Qe(c, "offsetHeight", (g) => ee(s, g)), I(e, c), xe();
}
var Rf = /* @__PURE__ */ we('<g pointer-events="none"><rect fill="none"></rect><rect fill="none"></rect></g>');
function ol(e, t) {
  let n = F(t, "color1", 3, "var(--color-black)"), r = F(t, "color2", 3, "var(--color-white)"), a = F(t, "strokeWidth", 3, 1), i = F(t, "strokeDashArray", 3, "4");
  var s = Rf(), o = b(s), u = m(o);
  ne(() => {
    M(s, "transform", `translate(${t.x ?? ""},${t.y ?? ""})`), M(o, "width", t.width), M(o, "height", t.height), M(o, "stroke-width", a()), M(o, "stroke", n()), M(u, "width", t.width), M(u, "height", t.height), M(u, "stroke-width", a()), M(u, "stroke", r()), M(u, "stroke-dasharray", i());
  }), I(e, s);
}
var zf = /* @__PURE__ */ te('<tr class="svelte-1u00ohp"><td class="svelte-1u00ohp"> </td><td class="svelte-1u00ohp"> </td></tr>'), If = /* @__PURE__ */ te('<table class="svelte-1u00ohp"><tbody class="svelte-1u00ohp"></tbody></table>');
function Tn(e, t) {
  var n = If(), r = b(n);
  ke(r, 21, () => t.data, ye, (a, i) => {
    let s = () => l(i).key, o = () => l(i).value;
    var u = zf(), f = b(u), v = b(f), c = m(f), d = b(c);
    ne(() => {
      de(v, s()), de(d, o());
    }), I(a, u);
  }), I(e, n);
}
var Df = /* @__PURE__ */ we('<rect class="sae-cm-cell"></rect><!>', 1), Of = /* @__PURE__ */ te('<div class="sae-cm-container svelte-kw462c"><svg><g></g><!><!></svg> <!> <!></div>');
function fl(e, t) {
  me(t, !0);
  let n = F(t, "showDifference", 3, !1), r = F(t, "marginTop", 3, 72), a = F(t, "marginRight", 3, 72), i = F(t, "marginBottom", 3, 72), s = F(t, "marginLeft", 3, 72), o = F(t, "legend", 3, "horizontal");
  function u(j, B, O, X, Q, U, re) {
    if (re === "none")
      return {
        svgWidth: j,
        svgHeight: B,
        legendWidth: 0,
        legendHeight: 0,
        legendMarginTop: 0,
        legendMarginRight: 0,
        legendMarginBottom: 0,
        legendMarginLeft: 0
      };
    if (re === "horizontal") {
      const K = Q - 16;
      return {
        svgWidth: j,
        svgHeight: B - K,
        legendWidth: j,
        legendHeight: K,
        legendMarginTop: 16,
        legendMarginRight: X,
        legendMarginBottom: 32,
        legendMarginLeft: U
      };
    } else {
      const K = X - 16;
      return {
        svgWidth: j - K,
        svgHeight: B,
        legendWidth: K,
        legendHeight: B,
        legendMarginTop: O,
        legendMarginRight: 60,
        legendMarginBottom: Q,
        legendMarginLeft: 0
      };
    }
  }
  const f = /* @__PURE__ */ x(() => u(t.width, t.height, r(), a(), i(), s(), o()));
  function v(j, B) {
    return B !== void 0 ? co(j.cells, B.cells).map(([O, X]) => ({
      ...O,
      pp_delta: O.pct - X.pct
    })) : j.cells.map((O) => ({ ...O, pp_delta: 0 }));
  }
  const c = /* @__PURE__ */ x(() => v(t.cm, t.other)), d = /* @__PURE__ */ x(() => Jn().domain(Se.value.label_indices).range([
    s(),
    t.width - a()
  ]).padding(0)), g = /* @__PURE__ */ x(() => Jn().domain(Se.value.label_indices).range([
    r(),
    t.height - i()
  ]).padding(0));
  function h(j, B) {
    if (B) {
      const [O, X] = Qs(j, (U) => U.pp_delta), Q = Math.max(Math.abs(O ?? 0), Math.abs(X ?? 0));
      return _a().domain([-Q, 0, Q]).interpolator(Sf);
    }
    return Ft().domain([0, lo(j, (O) => O.pct) ?? 0]).interpolator(Nf);
  }
  const _ = /* @__PURE__ */ x(() => h(l(c), n()));
  function w(j) {
    return Se.value.labels[j];
  }
  const T = ae.xs, k = 3, p = 6, y = /* @__PURE__ */ x(() => i() - T - k - p), S = /* @__PURE__ */ x(() => s() - T - k - p);
  let C = /* @__PURE__ */ se(null);
  function z(j, B, O) {
    ee(C, { data: B, anchor: j.currentTarget, index: O }, !0);
  }
  function H() {
    ee(C, null);
  }
  var V = Of();
  let J;
  var E = b(V), R = b(E);
  ke(R, 21, () => l(c), ye, (j, B, O) => {
    var X = Df();
    const Q = /* @__PURE__ */ x(() => n() ? l(_)(l(B).pp_delta) : l(_)(l(B).pct));
    var U = Ee(X), re = m(U);
    {
      var ie = (K) => {
        const he = /* @__PURE__ */ x(() => (l(d)(l(B).label) ?? 0) + 0.5), _e = /* @__PURE__ */ x(() => l(d).bandwidth() - 1), pe = /* @__PURE__ */ x(() => (l(g)(l(B).pred_label) ?? 0) + 1), Le = /* @__PURE__ */ x(() => l(g).bandwidth() - 1);
        ol(K, {
          get x() {
            return l(he);
          },
          get width() {
            return l(_e);
          },
          get y() {
            return l(pe);
          },
          get height() {
            return l(Le);
          }
        });
      };
      le(re, (K) => {
        var he;
        O === ((he = l(C)) == null ? void 0 : he.index) && K(ie);
      });
    }
    ne(
      (K, he, _e, pe) => {
        M(U, "x", K), M(U, "width", he), M(U, "y", _e), M(U, "height", pe), M(U, "fill", l(Q));
      },
      [
        () => (l(d)(l(B).label) ?? 0) + 0.5,
        () => l(d).bandwidth() - 1,
        () => (l(g)(l(B).pred_label) ?? 0) + 1,
        () => l(g).bandwidth() - 1
      ]
    ), Je("mouseenter", U, (K) => z(K, l(B), O)), Je("mouseleave", U, H), I(j, X);
  });
  var L = m(R);
  const q = /* @__PURE__ */ x(() => l(f).svgHeight - i()), A = /* @__PURE__ */ x(() => l(y) <= l(d).bandwidth() ? 0 : -45);
  Qt(L, {
    orientation: "bottom",
    get scale() {
      return l(d);
    },
    get translateY() {
      return l(q);
    },
    title: "True label",
    titleAnchor: "center",
    tickFormat: w,
    get tickLabelAngle() {
      return l(A);
    },
    get marginTop() {
      return r();
    },
    get marginRight() {
      return a();
    },
    get marginBottom() {
      return i();
    },
    get marginLeft() {
      return s();
    },
    get tickLabelFontSize() {
      return T;
    },
    tickPadding: k,
    tickLineSize: p,
    get maxTickLabelSpace() {
      return l(y);
    },
    get titleFontSize() {
      return ae.sm;
    }
  });
  var N = m(L);
  Qt(N, {
    orientation: "left",
    get scale() {
      return l(g);
    },
    get translateX() {
      return s();
    },
    title: "Predicted label",
    titleAnchor: "center",
    tickFormat: w,
    get marginTop() {
      return r();
    },
    get marginRight() {
      return a();
    },
    get marginBottom() {
      return i();
    },
    get marginLeft() {
      return s();
    },
    get tickLabelFontSize() {
      return T;
    },
    tickPadding: k,
    tickLineSize: p,
    get maxTickLabelSpace() {
      return l(S);
    },
    get titleFontSize() {
      return ae.sm;
    }
  });
  var Y = m(E, 2);
  {
    var D = (j) => {
      const B = /* @__PURE__ */ x(() => n() ? "Percentage point difference" : "Percent of data"), O = /* @__PURE__ */ x(() => n() ? ci : Jt);
      _n(j, {
        get width() {
          return l(f).legendWidth;
        },
        get height() {
          return l(f).legendHeight;
        },
        get color() {
          return l(_);
        },
        get orientation() {
          return o();
        },
        get marginTop() {
          return l(f).legendMarginTop;
        },
        get marginRight() {
          return l(f).legendMarginRight;
        },
        get marginBottom() {
          return l(f).legendMarginBottom;
        },
        get marginLeft() {
          return l(f).legendMarginLeft;
        },
        get title() {
          return l(B);
        },
        get tickLabelFontSize() {
          return T;
        },
        get titleFontSize() {
          return ae.sm;
        },
        get tickFormat() {
          return l(O);
        }
      });
    };
    le(Y, (j) => {
      o() !== "none" && j(D);
    });
  }
  var W = m(Y, 2);
  {
    var $ = (j) => {
      yr(j, xr(() => l(C), {
        children: (B, O) => {
          var X = qt(), Q = Ee(X);
          {
            var U = (re) => {
              const ie = /* @__PURE__ */ x(() => [
                {
                  key: "True label",
                  value: Se.value.labels[l(C).data.label]
                },
                {
                  key: "Predicted label",
                  value: Se.value.labels[l(C).data.pred_label]
                },
                {
                  key: "Percent of data",
                  value: Jt(l(C).data.pct)
                },
                {
                  key: "Instance count",
                  value: jt(l(C).data.count)
                },
                ...n() ? [
                  {
                    key: "Difference",
                    value: `${ci(l(C).data.pp_delta)} pp`
                  }
                ] : []
              ]);
              Tn(re, {
                get data() {
                  return l(ie);
                }
              });
            };
            le(Q, (re) => {
              l(C) && re(U);
            });
          }
          I(B, X);
        },
        $$slots: { default: !0 }
      }));
    };
    le(W, (j) => {
      l(C) && j($);
    });
  }
  ne(() => {
    J = Be(V, "", J, {
      "flex-direction": o() === "vertical" ? "row" : "column"
    }), M(E, "width", l(f).svgWidth), M(E, "height", l(f).svgHeight);
  }), I(e, V), xe();
}
var Bf = /* @__PURE__ */ we('<rect></rect><rect pointer-events="none"></rect>', 1), Hf = /* @__PURE__ */ te("<div><svg><g></g><!><!></svg> <!></div>");
function xa(e, t) {
  me(t, !0);
  let n = F(t, "marginLeft", 3, 0), r = F(t, "marginTop", 3, 0), a = F(t, "marginRight", 3, 0), i = F(t, "marginBottom", 3, 0), s = F(t, "xAxisLabel", 3, ""), o = F(t, "yAxisLabel", 3, ""), u = F(t, "showXAxis", 3, !0), f = F(t, "showYAxis", 3, !0), v = F(t, "xFormat", 3, Qr), c = F(t, "yFormat", 3, Qr), d = F(t, "tooltipEnabled", 3, !0), g = F(t, "tooltipData", 19, () => [
    {
      key: s(),
      value: (A, N, Y) => `${v()(A)} - ${v()(N)}`
    },
    {
      key: o(),
      value: (A, N, Y) => c()(Y)
    }
  ]), h = /* @__PURE__ */ x(() => Zt().domain([
    t.data.thresholds[0],
    t.data.thresholds[t.data.thresholds.length - 1]
  ]).range([
    n(),
    t.width - a()
  ])), _ = /* @__PURE__ */ x(() => Math.max(...t.data.counts)), w = /* @__PURE__ */ x(() => Zt().domain([0, l(_)]).nice().range([
    t.height - i(),
    r()
  ])), T = /* @__PURE__ */ x(() => ua(t.data.counts.length)), k = /* @__PURE__ */ x(() => Ki(t.data.thresholds)), p = /* @__PURE__ */ se(null);
  function y(A, N, Y, D, W) {
    ee(
      p,
      {
        count: N,
        xMin: Y,
        xMax: D,
        anchor: A.currentTarget,
        index: W
      },
      !0
    );
  }
  function S() {
    ee(p, null);
  }
  var C = Hf(), z = b(C), H = b(z);
  ke(H, 21, () => l(T), ye, (A, N) => {
    var Y = Bf(), D = Ee(Y), W = m(D);
    ne(
      ($, j, B, O, X, Q, U, re) => {
        var ie, K;
        M(D, "x", $), M(D, "width", j), M(D, "y", B), M(D, "height", O), M(D, "fill", l(N) === ((ie = l(p)) == null ? void 0 : ie.index) ? "var(--color-neutral-200)" : "var(--color-white)"), M(W, "x", X), M(W, "width", Q), M(W, "y", U), M(W, "height", re), M(W, "fill", l(N) === ((K = l(p)) == null ? void 0 : K.index) ? "var(--color-black)" : "var(--color-neutral-500)");
      },
      [
        () => l(h)(l(k)[l(N)][0]),
        () => Math.max(0, l(h)(l(k)[l(N)][1]) - l(h)(l(k)[l(N)][0])),
        () => l(w).range()[1],
        () => l(w).range()[0] - l(w).range()[1],
        () => l(h)(l(k)[l(N)][0]) + 0.5,
        () => Math.max(0, l(h)(l(k)[l(N)][1]) - l(h)(l(k)[l(N)][0]) - 1),
        () => l(w)(t.data.counts[l(N)]),
        () => l(w)(0) - l(w)(t.data.counts[l(N)])
      ]
    ), Je("mouseenter", D, function(...$) {
      var j;
      (j = d() ? (B) => y(B, t.data.counts[l(N)], l(k)[l(N)][0], l(k)[l(N)][1], l(N)) : null) == null || j.apply(this, $);
    }), Je("mouseleave", D, function(...$) {
      var j;
      (j = d() ? S : null) == null || j.apply(this, $);
    }), I(A, Y);
  });
  var V = m(H);
  {
    var J = (A) => {
      const N = /* @__PURE__ */ x(() => t.height - i());
      Qt(A, {
        orientation: "bottom",
        get scale() {
          return l(h);
        },
        get translateY() {
          return l(N);
        },
        get title() {
          return s();
        },
        titleAnchor: "right",
        get tickFormat() {
          return v();
        },
        get marginTop() {
          return r();
        },
        get marginRight() {
          return a();
        },
        get marginBottom() {
          return i();
        },
        get marginLeft() {
          return n();
        },
        numTicks: 5,
        get titleFontSize() {
          return ae.sm;
        },
        get tickLabelFontSize() {
          return ae.xs;
        },
        showDomain: !0
      });
    };
    le(V, (A) => {
      u() && A(J);
    });
  }
  var E = m(V);
  {
    var R = (A) => {
      Qt(A, {
        orientation: "left",
        get scale() {
          return l(w);
        },
        get translateX() {
          return n();
        },
        get title() {
          return o();
        },
        titleAnchor: "top",
        get tickFormat() {
          return c();
        },
        get marginTop() {
          return r();
        },
        get marginRight() {
          return a();
        },
        get marginBottom() {
          return i();
        },
        get marginLeft() {
          return n();
        },
        numTicks: 5,
        get titleFontSize() {
          return ae.sm;
        },
        get tickLabelFontSize() {
          return ae.xs;
        }
      });
    };
    le(E, (A) => {
      f() && A(R);
    });
  }
  var L = m(z, 2);
  {
    var q = (A) => {
      yr(A, xr(() => l(p), {
        children: (N, Y) => {
          const D = /* @__PURE__ */ x(() => g().map(({ key: W, value: $ }) => {
            var j, B, O;
            return {
              key: W,
              value: $(((j = l(p)) == null ? void 0 : j.xMin) ?? 0, ((B = l(p)) == null ? void 0 : B.xMax) ?? 0, ((O = l(p)) == null ? void 0 : O.count) ?? 0)
            };
          }));
          Tn(N, {
            get data() {
              return l(D);
            }
          });
        },
        $$slots: { default: !0 }
      }));
    };
    le(L, (A) => {
      l(p) && A(q);
    });
  }
  ne(() => {
    M(z, "width", t.width), M(z, "height", t.height);
  }), I(e, C), xe();
}
var jf = /* @__PURE__ */ te(`<div class="sae-info svelte-v66m4x">This histogram shows how often the features in the SAE activate.
              The activation rate is the percentage of instances that cause a
              feature to activate. Note that the x-axis uses a log scale.</div>`), Wf = /* @__PURE__ */ te('<div class="sae-overview-container svelte-v66m4x"><div class="sae-col svelte-v66m4x"><div class="sae-section svelte-v66m4x"><div class="sae-section-header svelte-v66m4x">Summary</div> <div class="sae-table-container svelte-v66m4x"><table class="svelte-v66m4x"><thead class="svelte-v66m4x"><tr><th colspan="2" class="svelte-v66m4x">Dataset</th></tr></thead><tbody><tr class="svelte-v66m4x"><td class="svelte-v66m4x">Instances</td><td class="svelte-v66m4x"> </td></tr><tr class="svelte-v66m4x"><td class="svelte-v66m4x">Tokens</td><td class="svelte-v66m4x"> </td></tr></tbody></table> <table class="svelte-v66m4x"><thead class="svelte-v66m4x"><tr><th colspan="2" class="svelte-v66m4x">Model</th></tr></thead><tbody><tr class="svelte-v66m4x"><td class="svelte-v66m4x">Error rate</td><td class="svelte-v66m4x"> </td></tr><tr class="svelte-v66m4x"><td class="svelte-v66m4x">Log loss</td><td class="svelte-v66m4x"> </td></tr></tbody></table> <table class="svelte-v66m4x"><thead class="svelte-v66m4x"><tr><th colspan="2" class="svelte-v66m4x">SAE</th></tr></thead><tbody><tr class="svelte-v66m4x"><td class="svelte-v66m4x">Total features</td><td class="svelte-v66m4x"> </td></tr><tr class="svelte-v66m4x"><td class="svelte-v66m4x">Inactive features</td><td class="svelte-v66m4x"> </td></tr></tbody></table></div></div> <div class="sae-section svelte-v66m4x"><div class="sae-section-header-row svelte-v66m4x"><div class="sae-section-header svelte-v66m4x">Feature activation rate distribution</div> <!></div> <div class="sae-vis svelte-v66m4x"><!></div></div></div> <div class="sae-col svelte-v66m4x"><div class="sae-section svelte-v66m4x"><div class="sae-section-header svelte-v66m4x">Confusion Matrix</div> <div class="sae-vis svelte-v66m4x"><!></div></div></div></div>');
function Vf(e, t) {
  me(t, !0);
  const n = /* @__PURE__ */ x(() => St.value.n_non_activating_features + St.value.n_dead_features), r = /* @__PURE__ */ x(() => l(n) / St.value.n_total_features);
  let a = /* @__PURE__ */ se(0), i = /* @__PURE__ */ se(0);
  const s = /* @__PURE__ */ x(() => ma(l(a), l(i), 1.6)), o = 8, u = 88, f = 80, v = 80;
  let c = /* @__PURE__ */ se(0), d = /* @__PURE__ */ se(0);
  const g = /* @__PURE__ */ x(() => ll(l(c), l(d), 1, o, u, f, v));
  var h = Wf(), _ = b(h), w = b(_), T = m(b(w), 2), k = b(T), p = m(b(k)), y = b(p), S = m(b(y)), C = b(S), z = m(y), H = m(b(z)), V = b(H), J = m(k, 2), E = m(b(J)), R = b(E), L = m(b(R)), q = b(L), A = m(R), N = m(b(A)), Y = b(N), D = m(J, 2), W = m(b(D)), $ = b(W), j = m(b($)), B = b(j), O = m($), X = m(b(O)), Q = b(X), U = m(w, 2);
  Be(U, "", {}, { flex: "1" });
  var re = b(U), ie = m(b(re), 2);
  Ye(ie, {
    position: "right",
    trigger: (Z) => {
      Ze(Z, {});
    },
    content: (Z) => {
      var fe = jf();
      I(Z, fe);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var K = m(re, 2), he = b(K);
  xa(he, {
    get data() {
      return St.value.sequence_act_rate_histogram;
    },
    marginTop: 20,
    marginRight: 20,
    marginLeft: 50,
    marginBottom: 40,
    get width() {
      return l(s).width;
    },
    get height() {
      return l(s).height;
    },
    xAxisLabel: "lg activation rate →",
    yAxisLabel: "↑ Feature count",
    tooltipData: [
      {
        key: "Feature count",
        value: (P, G, Z) => jt(Z)
      },
      {
        key: "Activation rate",
        value: (P, G, Z) => `${ir(10 ** P)} to ${ir(10 ** G)}`
      },
      {
        key: "Log 10 act. rate",
        value: (P, G, Z) => `${fi(P)} to ${fi(G)}`
      }
    ]
  });
  var _e = m(_, 2), pe = b(_e);
  Be(pe, "", {}, { flex: "1" });
  var Le = m(b(pe), 2), je = b(Le);
  fl(je, {
    get cm() {
      return Bt.value.cm;
    },
    legend: "vertical",
    get width() {
      return l(g).width;
    },
    get height() {
      return l(g).height;
    },
    marginTop: o,
    marginRight: u,
    marginBottom: f,
    marginLeft: v
  }), ne(
    (P, G, Z, fe, Me, Te, Ne) => {
      de(C, P), de(V, G), de(q, Z), de(Y, fe), de(B, Me), de(Q, `${Te ?? ""} (${Ne ?? ""})`);
    },
    [
      () => di(Se.value.n_sequences),
      () => di(Se.value.n_tokens),
      () => Jt(Bt.value.cm.error_pct),
      () => Cf(Bt.value.log_loss),
      () => jt(St.value.n_total_features),
      () => jt(l(n)),
      () => Jt(l(r))
    ]
  ), Qe(K, "offsetWidth", (P) => ee(a, P)), Qe(K, "offsetHeight", (P) => ee(i, P)), Qe(Le, "offsetWidth", (P) => ee(c, P)), Qe(Le, "offsetHeight", (P) => ee(d, P)), I(e, h), xe();
}
function Yf(e, t) {
  e.key === "Enter" && t();
}
var Xf = /* @__PURE__ */ te("<option> </option>"), Gf = (e, t) => t(e, "pred_label"), Uf = /* @__PURE__ */ te("<option> </option>"), Kf = /* @__PURE__ */ te("<option> </option>"), Zf = (e, t) => t(e, "true_label"), Qf = /* @__PURE__ */ te("<option> </option>"), Jf = /* @__PURE__ */ te("<option> </option>"), $f = /* @__PURE__ */ te('<label class="svelte-17fymm8"><span class="sae-title svelte-17fymm8">Predicted label:</span> <select class="svelte-17fymm8"><optgroup label="Wildcards"></optgroup><optgroup label="Labels"></optgroup></select></label> <label class="svelte-17fymm8"><span class="sae-title svelte-17fymm8">True label:</span> <select class="svelte-17fymm8"><optgroup label="Wildcards"></optgroup><optgroup label="Classes"></optgroup></select></label>', 1), eu = /* @__PURE__ */ te(
  `<p>The confusion matrix ranking orders the features based on the
              model's predictions on the instances that cause the features to
              activate.</p> <p> </p>`,
  1
), tu = /* @__PURE__ */ te('<div class="sae-info svelte-17fymm8"><!></div>'), nu = /* @__PURE__ */ te('<div class="sae-container svelte-17fymm8"><div class="sae-control-row svelte-17fymm8"><label class="svelte-17fymm8"><span class="sae-title svelte-17fymm8">Ranking:</span> <select class="svelte-17fymm8"></select></label> <!> <!></div> <div class="sae-control-row svelte-17fymm8"><div class="sae-feature-table-order svelte-17fymm8"><span class="sae-title svelte-17fymm8">Order:</span> <label class="svelte-17fymm8"><input type="radio" name="direction" class="svelte-17fymm8"/> <span>Ascending</span></label> <label class="svelte-17fymm8"><input type="radio" name="direction" class="svelte-17fymm8"/> <span>Descending</span></label></div> <div class="sae-feature-table-min-act-rate"><label class="svelte-17fymm8"><span class="sae-title svelte-17fymm8">Min. activation rate:</span> <input type="number" step="0.0001" class="svelte-17fymm8"/> <span>%</span></label></div></div></div>');
function ru(e, t) {
  me(t, !0);
  const n = [
    { label: "ID", value: "feature_id" },
    {
      label: "Activation Rate",
      value: "sequence_act_rate"
    },
    { label: "Confusion Matrix", value: "label" }
  ], r = [
    { label: "Any", value: "any" },
    { label: "Different", value: "different" }
  ], a = /* @__PURE__ */ x(() => Se.value.labels.map((R, L) => ({ label: R, value: `${L}` })));
  function i(R) {
    const L = R.currentTarget.value;
    L === "feature_id" ? ce.value = {
      kind: "feature_id",
      descending: ce.value.descending
    } : L === "sequence_act_rate" ? ce.value = {
      kind: "sequence_act_rate",
      descending: ce.value.descending
    } : ce.value = {
      kind: "label",
      true_label: "different",
      pred_label: "any",
      descending: ce.value.descending
    };
  }
  function s(R, L) {
    if (ce.value.kind !== "label")
      return;
    const q = R.currentTarget.value;
    ce.value = { ...ce.value, [L]: q };
  }
  function o(R) {
    const L = R.currentTarget.value;
    ce.value = {
      ...ce.value,
      descending: L === "descending"
    };
  }
  let u = /* @__PURE__ */ x(() => Vr.value * 100);
  function f() {
    Vr.value = l(u) / 100;
  }
  function v(R) {
    const { true_label: L, pred_label: q } = R, A = "Your current selection ranks the features by", N = "the percentage of instances where", Y = "any", D = "different", W = ($) => Se.value.labels[Number($)];
    return L === Y && q === Y || L === D && q === D ? `${A} their ID. Try another combination!` : L === Y && q === D || L === D && q === Y ? `${A} ${N} the model is wrong.` : L === Y ? `${A} ${N} the model predicts ${W(q)}.` : q === Y ? `${A} ${N} the true label is ${W(L)}.` : L === D ? `${A} ${N} the model incorrectly predicts ${W(q)}.` : q === D ? `${A} ${N} the true label is ${W(L)} and the model is incorrect.` : q === L ? `${A} ${N} the model correctly predicts ${W(L)}.` : `${A} ${N} the model predicts ${W(q)}, but the true label is ${W(L)}.`;
  }
  var c = nu(), d = b(c), g = b(d), h = m(b(g), 2);
  Cn(h, () => ce.value.kind);
  var _;
  h.__change = i, ke(h, 21, () => n, ye, (R, L) => {
    var q = Xf(), A = {}, N = b(q);
    ne(() => {
      A !== (A = l(L).value) && (q.value = (q.__value = l(L).value) ?? ""), de(N, l(L).label);
    }), I(R, q);
  });
  var w = m(g, 2);
  {
    var T = (R) => {
      var L = $f(), q = Ee(L), A = m(b(q), 2);
      Cn(A, () => ce.value.pred_label);
      var N;
      A.__change = [Gf, s];
      var Y = b(A);
      ke(Y, 21, () => r, ye, (X, Q) => {
        var U = Uf(), re = {}, ie = b(U);
        ne(() => {
          re !== (re = l(Q).value) && (U.value = (U.__value = l(Q).value) ?? ""), de(ie, l(Q).label);
        }), I(X, U);
      });
      var D = m(Y);
      ke(D, 21, () => l(a), ye, (X, Q) => {
        var U = Kf(), re = {}, ie = b(U);
        ne(() => {
          re !== (re = l(Q).value) && (U.value = (U.__value = l(Q).value) ?? ""), de(ie, l(Q).label);
        }), I(X, U);
      });
      var W = m(q, 2), $ = m(b(W), 2);
      Cn($, () => ce.value.true_label);
      var j;
      $.__change = [Zf, s];
      var B = b($);
      ke(B, 21, () => r, ye, (X, Q) => {
        var U = Qf(), re = {}, ie = b(U);
        ne(() => {
          re !== (re = l(Q).value) && (U.value = (U.__value = l(Q).value) ?? ""), de(ie, l(Q).label);
        }), I(X, U);
      });
      var O = m(B);
      ke(O, 21, () => l(a), ye, (X, Q) => {
        var U = Jf(), re = {}, ie = b(U);
        ne(() => {
          re !== (re = l(Q).value) && (U.value = (U.__value = l(Q).value) ?? ""), de(ie, l(Q).label);
        }), I(X, U);
      }), ne(() => {
        N !== (N = ce.value.pred_label) && (A.value = (A.__value = ce.value.pred_label) ?? "", Ot(A, ce.value.pred_label)), j !== (j = ce.value.true_label) && ($.value = ($.__value = ce.value.true_label) ?? "", Ot($, ce.value.true_label));
      }), I(R, L);
    };
    le(w, (R) => {
      ce.value.kind === "label" && R(T);
    });
  }
  var k = m(w, 2);
  Ye(k, {
    position: "bottom",
    trigger: (q) => {
      Ze(q, {});
    },
    content: (q) => {
      var A = tu(), N = b(A);
      {
        var Y = (W) => {
          var $ = Ca(`The ID ranking orders the features by their index in the SAE. This
            essentially provides a random order.`);
          I(W, $);
        }, D = (W, $) => {
          {
            var j = (O) => {
              var X = Ca(`The activation rate ranking orders the features by the percentage of
            instances in the dataset that cause them to activate.`);
              I(O, X);
            }, B = (O) => {
              var X = eu(), Q = m(Ee(X), 2), U = b(Q);
              ne((re) => de(U, re), [
                () => v(ce.value)
              ]), I(O, X);
            };
            le(
              W,
              (O) => {
                ce.value.kind === "sequence_act_rate" ? O(j) : O(B, !1);
              },
              $
            );
          }
        };
        le(N, (W) => {
          ce.value.kind === "feature_id" ? W(Y) : W(D, !1);
        });
      }
      I(q, A);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var p = m(d, 2), y = b(p), S = m(b(y), 2), C = b(S);
  za(C, "ascending"), C.__change = o;
  var z = m(S, 2), H = b(z);
  za(H, "descending"), H.__change = o;
  var V = m(y, 2), J = b(V), E = m(b(J), 2);
  E.__keydown = [Yf, f], Be(E, "", {}, { width: "7em" }), ne(() => {
    _ !== (_ = ce.value.kind) && (h.value = (h.__value = ce.value.kind) ?? "", Ot(h, ce.value.kind)), Ia(C, !ce.value.descending), Ia(H, ce.value.descending);
  }), Je("blur", E, () => f()), mr(E, () => l(u), (R) => ee(u, R)), I(e, c), xe();
}
Rt(["change", "keydown"]);
var au = /* @__PURE__ */ we('<rect></rect><rect pointer-events="none"></rect><!>', 1), iu = /* @__PURE__ */ te('<div class="sae-heatmap-container svelte-k83kh4"><div><!> <svg><!><!><g></g></svg></div> <!> <!></div>');
function ul(e, t) {
  me(t, !0);
  let n = F(t, "distribution", 3, null), r = F(t, "compareToBaseProbs", 3, !1), a = F(t, "maxColorDomain", 3, null), i = F(t, "marginTop", 3, 0), s = F(t, "marginRight", 3, 0), o = F(t, "marginBottom", 3, 0), u = F(t, "marginLeft", 3, 0), f = F(t, "xAxisLabel", 3, ""), v = F(t, "yAxisLabel", 3, ""), c = F(t, "showColorLegend", 3, !0), d = F(t, "showXAxis", 3, !0), g = F(t, "showYAxis", 3, !0), h = F(t, "tooltipEnabled", 3, !0);
  const _ = 16, w = /* @__PURE__ */ x(() => c() ? s() - _ : 0), T = /* @__PURE__ */ x(() => c() ? t.height : 0), k = /* @__PURE__ */ x(() => n() ? i() - 2 : 0), p = /* @__PURE__ */ x(() => i() - l(k)), y = /* @__PURE__ */ x(() => s() - l(w)), S = /* @__PURE__ */ x(() => t.width - l(w)), C = /* @__PURE__ */ x(() => t.height - l(k)), z = /* @__PURE__ */ x(() => c() ? i() : 0), H = /* @__PURE__ */ x(() => c() ? 64 : 0), V = /* @__PURE__ */ x(() => c() ? o() : 0), J = /* @__PURE__ */ x(() => 0), E = /* @__PURE__ */ x(() => t.marginalEffects.probs.map((P, G) => ({
    labelIndex: G,
    points: Ki(t.marginalEffects.thresholds).map(([Z, fe], Me) => {
      const Te = P[Me] >= 0 ? P[Me] : NaN, Ne = Number.isNaN(Te) ? NaN : Te - Bt.value.mean_pred_label_probs[G];
      return {
        startAct: Z,
        endAct: fe,
        prob: Te,
        delta: Ne
      };
    })
  })).filter((P, G) => t.classes.includes(G))), R = /* @__PURE__ */ x(() => Zt().domain([
    t.marginalEffects.thresholds[0],
    t.marginalEffects.thresholds[t.marginalEffects.thresholds.length - 1]
  ]).range([
    u(),
    l(S) - l(y)
  ])), L = /* @__PURE__ */ x(() => Jn().domain(t.classes).range([
    l(p),
    l(C) - o()
  ])), q = /* @__PURE__ */ x(() => a() ?? Math.max(...l(E).flatMap((P) => P.points.map((G) => Number.isNaN(G.prob) ? 0 : G.prob)))), A = /* @__PURE__ */ x(() => a() ?? Math.max(...l(E).flatMap((P) => P.points.map((G) => Math.abs(Number.isNaN(G.delta) ? 0 : G.delta))))), N = /* @__PURE__ */ x(() => Ft().domain([0, l(q)]).interpolator(il).unknown("var(--color-neutral-300)")), Y = /* @__PURE__ */ x(() => _a().domain([-l(A), 0, l(A)]).interpolator(Tf).unknown("var(--color-neutral-300)"));
  let D = /* @__PURE__ */ se(null);
  function W(P, G, Z, fe) {
    ee(
      D,
      {
        point: G,
        anchor: P.currentTarget,
        labelIndex: Z,
        pointIndex: fe
      },
      !0
    );
  }
  function $() {
    ee(D, null);
  }
  var j = iu(), B = b(j), O = b(B);
  {
    var X = (P) => {
      xa(P, {
        get data() {
          return n();
        },
        marginTop: 0,
        get marginRight() {
          return l(y);
        },
        get marginLeft() {
          return u();
        },
        marginBottom: 0,
        get width() {
          return l(S);
        },
        get height() {
          return l(k);
        },
        showXAxis: !1,
        showYAxis: !1,
        get xFormat() {
          return gt;
        },
        get tooltipEnabled() {
          return h();
        },
        get tooltipData() {
          return sl;
        }
      });
    };
    le(O, (P) => {
      n() && P(X);
    });
  }
  var Q = m(O, 2), U = b(Q);
  {
    var re = (P) => {
      const G = /* @__PURE__ */ x(() => l(C) - o());
      Qt(P, {
        orientation: "bottom",
        get scale() {
          return l(R);
        },
        get translateY() {
          return l(G);
        },
        get title() {
          return f();
        },
        get marginTop() {
          return l(p);
        },
        get marginRight() {
          return l(y);
        },
        get marginBottom() {
          return o();
        },
        get marginLeft() {
          return u();
        },
        numTicks: 5,
        get tickLabelFontSize() {
          return ae.xs;
        },
        get titleFontSize() {
          return ae.sm;
        }
      });
    };
    le(U, (P) => {
      d() && P(re);
    });
  }
  var ie = m(U);
  {
    var K = (P) => {
      Qt(P, {
        orientation: "left",
        get scale() {
          return l(L);
        },
        get translateX() {
          return u();
        },
        tickFormat: (G) => Se.value.labels[G],
        get title() {
          return v();
        },
        get marginTop() {
          return l(p);
        },
        get marginRight() {
          return l(y);
        },
        get marginBottom() {
          return o();
        },
        get marginLeft() {
          return u();
        },
        get tickLabelFontSize() {
          return ae.xs;
        },
        get titleFontSize() {
          return ae.sm;
        }
      });
    };
    le(ie, (P) => {
      g() && P(K);
    });
  }
  var he = m(ie);
  ke(he, 21, () => l(E), ye, (P, G) => {
    let Z = () => l(G).points, fe = () => l(G).labelIndex;
    var Me = qt(), Te = Ee(Me);
    ke(Te, 17, Z, ye, (Ne, ue, ve) => {
      var Ue = au(), Ae = Ee(Ue);
      M(Ae, "fill", "white");
      var _t = m(Ae), kr = m(_t);
      {
        var Mr = ($e) => {
          const ze = /* @__PURE__ */ x(() => l(R)(l(ue).startAct) + 0.5), an = /* @__PURE__ */ x(() => l(R)(l(ue).endAct) - l(R)(l(ue).startAct) - 1), Tr = /* @__PURE__ */ x(() => (l(L)(fe()) ?? 0) + 0.5), Ar = /* @__PURE__ */ x(() => l(L).bandwidth() - 1);
          ol($e, {
            get x() {
              return l(ze);
            },
            get width() {
              return l(an);
            },
            get y() {
              return l(Tr);
            },
            get height() {
              return l(Ar);
            }
          });
        };
        le(kr, ($e) => {
          var ze;
          fe() === ((ze = l(D)) == null ? void 0 : ze.labelIndex) && ve === l(D).pointIndex && $e(Mr);
        });
      }
      ne(
        ($e, ze, an, Tr, Ar, cl, dl, vl, gl) => {
          M(Ae, "x", $e), M(Ae, "width", ze), M(Ae, "y", an), M(Ae, "height", Tr), M(_t, "x", Ar), M(_t, "width", cl), M(_t, "y", dl), M(_t, "height", vl), M(_t, "fill", gl);
        },
        [
          () => l(R)(l(ue).startAct),
          () => l(R)(l(ue).endAct) - l(R)(l(ue).startAct),
          () => l(L)(fe()) ?? 0,
          () => l(L).bandwidth(),
          () => l(R)(l(ue).startAct) + 0.5,
          () => l(R)(l(ue).endAct) - l(R)(l(ue).startAct) - 1,
          () => (l(L)(fe()) ?? 0) + 0.5,
          () => l(L).bandwidth() - 1,
          () => r() ? l(Y)(l(ue).delta) : l(N)(l(ue).prob)
        ]
      ), Je("mouseenter", Ae, function(...$e) {
        var ze;
        (ze = h() ? (an) => W(an, l(ue), fe(), ve) : null) == null || ze.apply(this, $e);
      }), Je("mouseleave", Ae, function(...$e) {
        var ze;
        (ze = h() ? $ : null) == null || ze.apply(this, $e);
      }), I(Ne, Ue);
    }), I(P, Me);
  });
  var _e = m(B, 2);
  {
    var pe = (P) => {
      const G = /* @__PURE__ */ x(() => r() ? l(Y) : l(N)), Z = /* @__PURE__ */ x(() => r() ? "Difference from base prob." : "Mean predicted probability");
      _n(P, {
        get width() {
          return l(w);
        },
        get height() {
          return l(T);
        },
        get color() {
          return l(G);
        },
        orientation: "vertical",
        get marginTop() {
          return l(z);
        },
        get marginRight() {
          return l(H);
        },
        get marginBottom() {
          return l(V);
        },
        marginLeft: l(J),
        get title() {
          return l(Z);
        },
        get tickLabelFontSize() {
          return ae.xs;
        },
        get titleFontSize() {
          return ae.sm;
        },
        get tickFormat() {
          return Qr;
        }
      });
    };
    le(_e, (P) => {
      c() && P(pe);
    });
  }
  var Le = m(_e, 2);
  {
    var je = (P) => {
      yr(P, xr(() => l(D), {
        children: (G, Z) => {
          var fe = qt(), Me = Ee(fe);
          {
            var Te = (Ne) => {
              const ue = /* @__PURE__ */ x(() => [
                {
                  key: "Activation value",
                  value: `${gt(l(D).point.startAct)} to ${gt(l(D).point.endAct)}`
                },
                {
                  key: "Predicted label",
                  value: Se.value.labels[l(D).labelIndex]
                },
                {
                  key: "Mean probability",
                  value: Number.isNaN(l(D).point.prob) ? "No data" : ui(l(D).point.prob)
                },
                ...r() ? [
                  {
                    key: "Diff. from base prob.",
                    value: ui(l(D).point.delta)
                  }
                ] : []
              ]);
              Tn(Ne, {
                get data() {
                  return l(ue);
                }
              });
            };
            le(Me, (Ne) => {
              l(D) && Ne(Te);
            });
          }
          I(G, fe);
        },
        $$slots: { default: !0 }
      }));
    };
    le(Le, (P) => {
      l(D) && P(je);
    });
  }
  ne(() => {
    M(Q, "width", l(S)), M(Q, "height", l(C));
  }), I(e, j), xe();
}
var lu = /* @__PURE__ */ te('<div class="sae-token svelte-165qlb"><span class="sae-token-name svelte-165qlb"> </span></div>'), su = /* @__PURE__ */ te('<div class="sae-sequence svelte-165qlb"><!> <!></div>');
function pa(e, t) {
  me(t, !0);
  let n = F(t, "tooltipEnabled", 3, !0), r = F(t, "hidePadding", 3, !1), a = /* @__PURE__ */ se(null);
  function i(d, g, h) {
    ee(a, { data: g, anchor: d.currentTarget, index: h }, !0);
  }
  function s() {
    ee(a, null);
  }
  var o = su();
  let u;
  var f = b(o);
  ke(f, 17, () => t.sequence.display_tokens, ye, (d, g, h) => {
    var _ = qt(), w = Ee(_);
    {
      var T = (k) => {
        var p = lu();
        const y = /* @__PURE__ */ x(() => l(g).max_act > 0 ? t.colorScale(l(g).max_act) : "var(--color-white)");
        let S;
        var C = b(p), z = b(C);
        ne(() => {
          var H;
          S = Be(p, "", S, {
            "--token-color": l(y),
            "font-weight": h === t.sequence.max_token_index && l(g).max_act > 0 ? "var(--font-bold)" : "var(--font-normal)",
            "background-color": n() && ((H = l(a)) == null ? void 0 : H.index) === h ? "var(--color-neutral-300)" : "var(--color-white)"
          }), de(z, l(g).display);
        }), Je("mouseenter", p, function(...H) {
          var V;
          (V = n() ? (J) => i(J, l(g), h) : null) == null || V.apply(this, H);
        }), Je("mouseleave", p, function(...H) {
          var V;
          (V = n() ? s : null) == null || V.apply(this, H);
        }), I(k, p);
      };
      le(w, (k) => {
        r() && l(g).is_padding || k(T);
      });
    }
    I(d, _);
  });
  var v = m(f, 2);
  {
    var c = (d) => {
      yr(d, xr(() => l(a), {
        children: (g, h) => {
          var _ = qt(), w = Ee(_);
          {
            var T = (k) => {
              const p = /* @__PURE__ */ x(() => [
                {
                  key: "Token",
                  value: l(a).data.display
                },
                {
                  key: "Activation",
                  value: gt(l(a).data.max_act)
                }
              ]);
              Tn(k, {
                get data() {
                  return l(p);
                }
              });
            };
            le(w, (k) => {
              l(a) && k(T);
            });
          }
          I(g, _);
        },
        $$slots: { default: !0 }
      }));
    };
    le(v, (d) => {
      l(a) && d(c);
    });
  }
  ne(() => u = Be(o, "", u, { "flex-wrap": t.wrap ? "wrap" : "nowrap" })), I(e, o), xe();
}
function ou(e, t, n) {
  return e < t ? t : e > n ? n : e;
}
function fu(e, t, n) {
  e.key === "Enter" && t(l(n) - 1);
}
var uu = (e, t, n) => t(l(n) - 2), cu = (e, t, n) => t(l(n)), du = /* @__PURE__ */ te('<div class="sae-page-container svelte-1rue4kd"><button class="svelte-1rue4kd">←</button> <div class="sae-page-select svelte-1rue4kd"><span>Page</span> <input type="number" class="svelte-1rue4kd"/> <span>/</span> <span> </span></div> <button class="svelte-1rue4kd">→</button></div>');
function vu(e, t) {
  me(t, !0);
  let n = /* @__PURE__ */ x(() => It.value + 1);
  const r = /* @__PURE__ */ x(() => Math.log10(fn.value + 1) + 1);
  function a(g) {
    const h = ou(g, 0, fn.value);
    h === It.value ? ee(n, h + 1) : It.value = h;
  }
  var i = du(), s = b(i);
  s.__click = [uu, a, n];
  var o = m(s, 2), u = m(b(o), 2);
  u.__keydown = [
    fu,
    a,
    n
  ];
  let f;
  var v = m(u, 4), c = b(v), d = m(o, 2);
  d.__click = [cu, a, n], ne(() => {
    s.disabled = It.value <= 0, f = Be(u, "", f, { width: `${l(r) ?? ""}em` }), de(c, fn.value + 1), d.disabled = It.value >= fn.value;
  }), Je("blur", u, () => a(l(n) - 1)), mr(u, () => l(n), (g) => ee(n, g)), I(e, i), xe();
}
Rt(["click", "keydown"]);
var gu = /* @__PURE__ */ te('<div class="sae-info svelte-1g7tfe9">The index of the feature in the SAE.</div>'), hu = /* @__PURE__ */ te(`<div class="sae-info svelte-1g7tfe9">The model's error rate on instances that activate the feature.</div>`), bu = /* @__PURE__ */ te('<div class="sae-info svelte-1g7tfe9">The percentage of instances that activate the feature.</div>'), _u = /* @__PURE__ */ te(`<div class="sae-info svelte-1g7tfe9">A histogram of the feature's instance-level activation values.</div>`), mu = /* @__PURE__ */ te(`<div class="sae-info sae-probabilities-info svelte-1g7tfe9"><div>The probabilities of the top classes for instances that activate
              the feature. The x-axis encodes the activation value.</div> <!></div>`), xu = /* @__PURE__ */ te(`<div class="sae-info sae-example-info svelte-1g7tfe9"><div>The token that maximally activates the feature and its surrounding
              context.</div> <!></div>`), pu = (e, t, n) => t.onClickFeature(l(n).feature_id), wu = /* @__PURE__ */ te('<div><div><button class="sae-table-feature-id-btn svelte-1g7tfe9"> </button></div></div> <div><div> </div></div> <div><div> </div></div> <div><!></div> <div><!></div> <div><!></div>', 1), yu = /* @__PURE__ */ te('<div class="sae-table-container svelte-1g7tfe9"><div class="sae-table-controls"><!></div> <div class="sae-table svelte-1g7tfe9"><div class="sae-table-cell sae-table-header sae-table-header-align-right svelte-1g7tfe9"><span class="svelte-1g7tfe9">ID</span> <!></div> <div class="sae-table-cell sae-table-header sae-table-header-align-right svelte-1g7tfe9"><span class="svelte-1g7tfe9">Err. Rate</span> <!></div> <div class="sae-table-cell sae-table-header sae-table-header-align-right svelte-1g7tfe9"><span class="svelte-1g7tfe9">Act. Rate</span> <!></div> <div class="sae-table-cell sae-table-header sae-table-header-align-right svelte-1g7tfe9"><span class="svelte-1g7tfe9">Act. Distribution</span> <!></div> <div class="sae-table-cell sae-table-header sae-table-header-align-right svelte-1g7tfe9"><span class="svelte-1g7tfe9">Top Class Probabilities</span> <!></div> <div class="sae-table-cell sae-table-header svelte-1g7tfe9"><span class="svelte-1g7tfe9">Example</span> <!></div> <!></div> <div class="sae-table-pagination"><!></div></div>');
function ku(e, t) {
  me(t, !0);
  const n = /* @__PURE__ */ x(() => ae.base * 0.5), r = /* @__PURE__ */ x(() => ae.base * 0.25), a = /* @__PURE__ */ x(() => ae.base * 3), i = /* @__PURE__ */ x(() => l(a) * 3), s = 80;
  function o(L) {
    return L.mean_pred_label_probs.map((q, A) => ({ prob: q, label: A })).sort((q, A) => Gi(q.prob, A.prob)).slice(0, 3).map(({ label: q }) => q);
  }
  const u = !0;
  var f = yu(), v = b(f), c = b(v);
  ru(c, {});
  var d = m(v, 2);
  let g;
  var h = b(d), _ = m(b(h), 2);
  Ye(_, {
    position: "right",
    trigger: (A) => {
      Ze(A, {});
    },
    content: (A) => {
      var N = gu();
      I(A, N);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var w = m(h, 2), T = m(b(w), 2);
  Ye(T, {
    position: "right",
    trigger: (A) => {
      Ze(A, {});
    },
    content: (A) => {
      var N = hu();
      I(A, N);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var k = m(w, 2), p = m(b(k), 2);
  Ye(p, {
    position: "right",
    trigger: (A) => {
      Ze(A, {});
    },
    content: (A) => {
      var N = bu();
      I(A, N);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var y = m(k, 2), S = m(b(y), 2);
  Ye(S, {
    position: "right",
    trigger: (A) => {
      Ze(A, {});
    },
    content: (A) => {
      var N = _u();
      I(A, N);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var C = m(y, 2), z = m(b(C), 2);
  Ye(z, {
    position: "right",
    trigger: (A) => {
      Ze(A, {});
    },
    content: (A) => {
      var N = mu(), Y = m(b(N), 2);
      const D = /* @__PURE__ */ x(() => Ft([0, 1], il)), W = /* @__PURE__ */ x(() => ae.sm * 16), $ = /* @__PURE__ */ x(() => ae.sm * 2), j = /* @__PURE__ */ x(() => ae.sm * 2);
      _n(Y, {
        get color() {
          return l(D);
        },
        get width() {
          return l(W);
        },
        height: 56,
        orientation: "horizontal",
        title: "Mean predicted probability",
        marginTop: 18,
        marginBottom: 24,
        get marginLeft() {
          return l($);
        },
        get marginRight() {
          return l(j);
        },
        get titleFontSize() {
          return ae.sm;
        },
        get tickLabelFontSize() {
          return ae.xs;
        }
      }), I(A, N);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var H = m(C, 2), V = m(b(H), 2);
  Ye(V, {
    position: "right",
    trigger: (A) => {
      Ze(A, {});
    },
    content: (A) => {
      var N = xu(), Y = m(b(N), 2);
      const D = /* @__PURE__ */ x(() => Ft([0, 1], (B) => Zr(1 - B))), W = /* @__PURE__ */ x(() => ae.sm * 16), $ = /* @__PURE__ */ x(() => ae.sm * 2), j = /* @__PURE__ */ x(() => ae.sm * 2);
      _n(Y, {
        get color() {
          return l(D);
        },
        get width() {
          return l(W);
        },
        height: 56,
        orientation: "horizontal",
        title: "Activation value",
        marginTop: 18,
        marginBottom: 24,
        get marginLeft() {
          return l($);
        },
        get marginRight() {
          return l(j);
        },
        get titleFontSize() {
          return ae.sm;
        },
        get tickLabelFontSize() {
          return ae.xs;
        },
        tickValues: [0, 1],
        tickFormat: (B) => B === 0 ? "Min" : B === 1 ? "Max" : ""
      }), I(A, N);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var J = m(H, 2);
  ke(J, 17, () => Yr.value, ye, (L, q, A) => {
    var N = wu();
    const Y = /* @__PURE__ */ x(() => A !== Yr.value.length - 1);
    var D = Ee(N);
    let W;
    var $ = b(D), j = b($);
    j.__click = [pu, t, q];
    var B = b(j), O = m(D, 2);
    let X;
    var Q = b(O), U = b(Q), re = m(O, 2);
    let ie;
    var K = b(re), he = b(K), _e = m(re, 2);
    let pe;
    var Le = b(_e);
    xa(Le, {
      get data() {
        return l(q).sequence_acts_histogram;
      },
      get width() {
        return l(i);
      },
      get height() {
        return l(a);
      },
      tooltipEnabled: u,
      get tooltipData() {
        return sl;
      }
    });
    var je = m(_e, 2);
    let P;
    var G = b(je);
    const Z = /* @__PURE__ */ x(() => o(l(q))), fe = /* @__PURE__ */ x(() => l(i) + s);
    ul(G, {
      get marginalEffects() {
        return l(q).marginal_effects;
      },
      get classes() {
        return l(Z);
      },
      get width() {
        return l(fe);
      },
      get height() {
        return l(a);
      },
      maxColorDomain: 1,
      showColorLegend: !1,
      marginTop: 0,
      marginRight: 0,
      marginBottom: 0,
      marginLeft: s,
      showXAxis: !1,
      showYAxis: !0,
      tooltipEnabled: u
    });
    var Me = m(je, 2);
    let Te;
    var Ne = b(Me);
    const ue = /* @__PURE__ */ x(() => Ft([0, l(q).max_act], (ve) => Zr(1 - ve)));
    pa(Ne, {
      get colorScale() {
        return l(ue);
      },
      get sequence() {
        return l(q).sequence_intervals[0].sequences[0];
      },
      wrap: !1,
      tooltipEnabled: u
    }), ne(
      (ve, Ue, Ae, _t, kr, Mr, $e, ze) => {
        W = qe(D, 1, "sae-table-cell sae-table-number-value svelte-1g7tfe9", null, W, ve), de(B, l(q).feature_id), X = qe(O, 1, "sae-table-cell sae-table-number-value svelte-1g7tfe9", null, X, Ue), de(U, Ae), ie = qe(re, 1, "sae-table-cell sae-table-number-value svelte-1g7tfe9", null, ie, _t), de(he, kr), pe = qe(_e, 1, "sae-table-cell svelte-1g7tfe9", null, pe, Mr), P = qe(je, 1, "sae-table-cell svelte-1g7tfe9", null, P, $e), Te = qe(Me, 1, "sae-table-cell sae-table-example-sequence svelte-1g7tfe9", null, Te, ze);
      },
      [
        () => ({ "sae-table-border": l(Y) }),
        () => ({ "sae-table-border": l(Y) }),
        () => Jt(l(q).cm.error_pct),
        () => ({ "sae-table-border": l(Y) }),
        () => ir(l(q).sequence_act_rate),
        () => ({ "sae-table-border": l(Y) }),
        () => ({ "sae-table-border": l(Y) }),
        () => ({ "sae-table-border": l(Y) })
      ]
    ), I(L, N);
  });
  var E = m(d, 2), R = b(E);
  vu(R, {}), ne(() => g = Be(d, "", g, {
    "--cell-padding-x": `${l(n) ?? ""}px`,
    "--cell-padding-y": `${l(r) ?? ""}px`
  })), I(e, f), xe();
}
Rt(["click"]);
var Mu = /* @__PURE__ */ we('<svg stroke-width="2" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" color="currentcolor"><path d="M12 11.5V16.5" stroke="currentcolor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path><path d="M12 7.51L12.01 7.49889" stroke="currentcolor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path><path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentcolor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>');
function Tu(e, t) {
  me(t, !0);
  let n = F(t, "width", 19, () => ae.base), r = F(t, "height", 19, () => ae.base);
  var a = Mu();
  ne(() => {
    M(a, "width", n()), M(a, "height", r());
  }), I(e, a), xe();
}
var Au = /* @__PURE__ */ te(`<div class="sae-info svelte-w9fu8s">This section shows snippets of instances that activate the
              feature.</div>`), Su = /* @__PURE__ */ te("<option> </option>"), Eu = /* @__PURE__ */ te("<div><!></div> <div> </div> <div> </div> <div><!></div>", 1), Lu = /* @__PURE__ */ te('<div class="sae-sequence-container svelte-w9fu8s"><div class="sae-sequences-header svelte-w9fu8s"><div class="sae-sequences-controls svelte-w9fu8s"><div class="sae-info svelte-w9fu8s"><span class="svelte-w9fu8s">Example Activations</span> <!></div> <label class="svelte-w9fu8s"><span>Range:</span> <select class="svelte-w9fu8s"><option>Max activations</option><!></select></label> <label class="svelte-w9fu8s"><input type="checkbox"/> <span>Wrap text</span></label></div> <div class="sae-sequences-color-legend"><!></div></div> <div class="sae-sequences-table svelte-w9fu8s"><div class="sae-sequences-table-cell sae-sequences-table-header svelte-w9fu8s"></div> <div class="sae-sequences-table-cell sae-sequences-table-header svelte-w9fu8s">Pred.</div> <div class="sae-sequences-table-cell sae-sequences-table-header svelte-w9fu8s">True</div> <div class="sae-sequences-table-cell sae-sequences-table-header svelte-w9fu8s">Tokens</div> <!></div></div>');
function Nu(e, t) {
  me(t, !0);
  let n = /* @__PURE__ */ x(() => rt.value.sequence_intervals[In.value]);
  function r(p) {
    const y = Object.entries(p.extras).map(([S, C]) => ({ key: S, value: C }));
    return [
      {
        key: "Instance index",
        value: `${p.sequence_index}`
      },
      ...y
    ];
  }
  var a = Lu(), i = b(a), s = b(i), o = b(s), u = m(b(o), 2);
  Ye(u, {
    position: "right",
    trigger: (S) => {
      Ze(S, {});
    },
    content: (S) => {
      var C = Au();
      I(S, C);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var f = m(o, 2), v = m(b(f), 2), c = b(v);
  c.value = c.__value = 0;
  var d = m(c);
  ke(d, 17, () => ua(rt.value.sequence_intervals.length - 1, 0, -1), ye, (p, y) => {
    var S = Su();
    const C = /* @__PURE__ */ x(() => rt.value.sequence_intervals[l(y)]);
    var z = {}, H = b(S);
    ne(
      (V, J) => {
        z !== (z = l(y)) && (S.value = (S.__value = l(y)) ?? ""), de(H, `${V ?? ""} to ${J ?? ""}`);
      },
      [
        () => gt(l(C).min_max_act),
        () => gt(l(C).max_max_act)
      ]
    ), I(p, S);
  });
  var g = m(f, 2), h = b(g), _ = m(s, 2), w = b(_);
  _n(w, {
    width: 256,
    height: 56,
    get color() {
      return t.tokenColor;
    },
    orientation: "horizontal",
    title: "Activation value",
    marginTop: 18,
    marginBottom: 24,
    get titleFontSize() {
      return ae.sm;
    },
    get tickLabelFontSize() {
      return ae.xs;
    },
    tickFormat: (p) => p === 0 ? "> 0" : gt(p)
  });
  var T = m(i, 2), k = m(b(T), 8);
  ke(k, 17, () => l(n).sequences, ye, (p, y, S) => {
    var C = Eu();
    const z = /* @__PURE__ */ x(() => S !== l(n).sequences.length - 1);
    var H = Ee(C);
    let V;
    var J = b(H);
    Ye(J, {
      position: "left",
      trigger: (B) => {
        Tu(B, {});
      },
      content: (B) => {
        const O = /* @__PURE__ */ x(() => r(l(y)));
        Tn(B, {
          get data() {
            return l(O);
          }
        });
      },
      $$slots: { trigger: !0, content: !0 }
    });
    var E = m(H, 2);
    let R;
    var L = b(E), q = m(E, 2);
    let A;
    var N = b(q), Y = m(q, 2);
    let D;
    var W = b(Y);
    pa(W, {
      get colorScale() {
        return t.tokenColor;
      },
      get sequence() {
        return l(y);
      },
      get wrap() {
        return zn.value;
      },
      hidePadding: !1
    }), ne(
      ($, j, B, O) => {
        V = qe(H, 1, "sae-sequences-table-cell svelte-w9fu8s", null, V, $), R = qe(E, 1, "sae-sequences-table-cell svelte-w9fu8s", null, R, j), de(L, Se.value.labels[l(y).pred_label]), A = qe(q, 1, "sae-sequences-table-cell svelte-w9fu8s", null, A, B), de(N, Se.value.labels[l(y).label]), D = qe(Y, 1, "sae-sequences-table-cell sae-sequences-table-tokens svelte-w9fu8s", null, D, O);
      },
      [
        () => ({
          "sae-sequences-table-border": l(z)
        }),
        () => ({
          "sae-sequences-table-border": l(z)
        }),
        () => ({
          "sae-sequences-table-border": l(z)
        }),
        () => ({
          "sae-sequences-table-border": l(z)
        })
      ]
    ), I(p, C);
  }), Ns(v, () => In.value, (p) => In.value = p), vn(h, () => zn.value, (p) => zn.value = p), I(e, a), xe();
}
function Fu(e, t) {
  e.key === "Enter" && t();
}
var Cu = /* @__PURE__ */ te(`<div class="sae-info svelte-cfsok5">Enter some text and check to see if it causes the feature to
            activate. Special tokens are automatically added.</div>`), qu = /* @__PURE__ */ te('<div class="sae-sequences-table svelte-cfsok5"><div class="sae-sequences-table-cell sae-sequences-table-header svelte-cfsok5">Pred.</div> <div class="sae-sequences-table-cell sae-sequences-table-header svelte-cfsok5">Prob.</div> <div class="sae-sequences-table-cell sae-sequences-table-header svelte-cfsok5">Tokens</div> <div> </div> <div> </div> <div><!></div></div>'), Pu = /* @__PURE__ */ te('<div class="sae-feature-testing-container svelte-cfsok5"><div class="sae-controls svelte-cfsok5"><div class="sae-title svelte-cfsok5"><span class="svelte-cfsok5">Test Feature</span> <!></div> <label class="svelte-cfsok5"><input type="checkbox"/> <span>Hide padding</span></label> <label class="svelte-cfsok5"><input type="checkbox"/> <span>Wrap text</span></label></div> <div class="sae-input-row svelte-cfsok5"><input type="text" class="svelte-cfsok5"/> <button>Test</button></div> <!></div>');
function Ru(e, t) {
  me(t, !0);
  let n = /* @__PURE__ */ x(() => t.featureId === qn.value.feature_index ? qn.value.sequence : "");
  function r() {
    qn.value = {
      feature_index: t.featureId,
      sequence: l(n)
    };
  }
  var a = Pu(), i = b(a), s = b(i), o = m(b(s), 2);
  Ye(o, {
    position: "right",
    trigger: (p) => {
      Ze(p, {});
    },
    content: (p) => {
      var y = Cu();
      I(p, y);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var u = m(s, 2), f = b(u), v = m(u, 2), c = b(v), d = m(i, 2), g = b(d);
  g.__keydown = [Fu, r];
  var h = m(g, 2);
  h.__click = r;
  var _ = m(d, 2);
  {
    var w = (T) => {
      var k = qu(), p = m(b(k), 6);
      qe(p, 1, "sae-sequences-table-cell svelte-cfsok5", null, {}, { "sae-sequences-table-border": !0 });
      var y = b(p), S = m(p, 2);
      qe(S, 1, "sae-sequences-table-cell svelte-cfsok5", null, {}, { "sae-sequences-table-border": !0 });
      var C = b(S), z = m(S, 2);
      qe(z, 1, "sae-sequences-table-cell sae-sequences-table-tokens svelte-cfsok5", null, {}, { "sae-sequences-table-border": !0 });
      var H = b(z);
      pa(H, {
        get colorScale() {
          return t.tokenColor;
        },
        get sequence() {
          return Dt.value;
        },
        get wrap() {
          return Dn.value;
        },
        get hidePadding() {
          return On.value;
        }
      }), ne(
        (V) => {
          de(y, Se.value.labels[Dt.value.pred_label]), de(C, V);
        },
        [
          () => Jt(Dt.value.pred_probs[Dt.value.pred_label])
        ]
      ), I(T, k);
    };
    le(_, (T) => {
      Dt.value.feature_index === t.featureId && T(w);
    });
  }
  vn(f, () => On.value, (T) => On.value = T), vn(c, () => Dn.value, (T) => Dn.value = T), mr(g, () => l(n), (T) => ee(n, T)), I(e, a), xe();
}
Rt(["keydown", "click"]);
function zu(e, t) {
  e.key === "Enter" && t();
}
var Iu = /* @__PURE__ */ te('<div class="sae-info svelte-1vkzfjf"></div>'), Du = /* @__PURE__ */ te('<div class="sae-info svelte-1vkzfjf"></div>'), Ou = /* @__PURE__ */ te('<div class="sae-inference-container svelte-1vkzfjf"><!></div>'), Bu = /* @__PURE__ */ te('<div class="sae-container svelte-1vkzfjf"><div class="sae-controls svelte-1vkzfjf"><div class="sae-feature-input svelte-1vkzfjf"><label class="svelte-1vkzfjf"><span>Feature ID:</span> <input type="number" class="svelte-1vkzfjf"/></label> <button class="svelte-1vkzfjf">Go</button></div> <div><span>Activation Rate:</span> <span> </span></div></div> <div><div class="sae-effects-container svelte-1vkzfjf"><div class="sae-effects-controls svelte-1vkzfjf"><div class="sae-title svelte-1vkzfjf"><span class="svelte-1vkzfjf">Predicted Probabilities</span> <!></div> <label class="svelte-1vkzfjf"><input type="checkbox"/> <span></span></label></div> <div class="sae-effects-vis svelte-1vkzfjf"><!></div></div> <div class="sae-cm-container svelte-1vkzfjf"><div class="sae-cm-controls svelte-1vkzfjf"><div class="sae-title svelte-1vkzfjf"><span class="svelte-1vkzfjf">Confusion Matrix</span> <!></div> <label class="svelte-1vkzfjf"><input type="checkbox"/> <span></span></label></div> <div class="sae-cm-vis svelte-1vkzfjf"><!></div></div> <div class="sae-sequences-container svelte-1vkzfjf"><!></div> <!></div></div>');
function Hu(e, t) {
  me(t, !0);
  const n = /* @__PURE__ */ x(() => Math.log10(St.value.n_total_features) + 1), r = /* @__PURE__ */ x(() => Ft().domain([0, rt.value.max_act]).interpolator((P) => Zr(1 - P)));
  let a = /* @__PURE__ */ x(() => cn.value);
  function i() {
    cn.value = l(a);
  }
  let s = /* @__PURE__ */ se(0), o = /* @__PURE__ */ se(0), u = /* @__PURE__ */ x(() => ma(l(o), l(s), 1.6));
  const f = 8, v = 88, c = 80, d = 80;
  let g = /* @__PURE__ */ se(0), h = /* @__PURE__ */ se(0);
  const _ = /* @__PURE__ */ x(() => ll(l(g), l(h), 1, f, v, c, d));
  var w = Bu(), T = b(w), k = b(T), p = b(k), y = b(p);
  Be(y, "", {}, { "font-weight": "var(--font-medium)" });
  var S = m(y, 2);
  S.__keydown = [zu, i];
  let C;
  var z = m(p, 2);
  z.__click = i;
  var H = m(k, 2), V = b(H);
  Be(V, "", {}, { "font-weight": "var(--font-medium)" });
  var J = m(V, 2), E = b(J), R = m(T, 2), L = b(R), q = b(L), A = b(q), N = m(b(A), 2);
  Ye(N, {
    position: "right",
    trigger: (Z) => {
      Ze(Z, {});
    },
    content: (Z) => {
      var fe = Iu();
      fe.textContent = `Each cell in the heatmap shows the model's mean predicted
                probability for the given class on instances that cause the
                feature to activate in the given range. Checking "Compare to base probabilities"
                shows the difference relative to the model's mean predicted
                probabilities for the entire dataset.`, I(Z, fe);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var Y = m(A, 2), D = b(Y), W = m(D, 2);
  W.textContent = "Compare to base probabilities";
  var $ = m(q, 2), j = b($);
  ul(j, {
    get marginalEffects() {
      return rt.value.marginal_effects;
    },
    get distribution() {
      return rt.value.sequence_acts_histogram;
    },
    get classes() {
      return Se.value.label_indices;
    },
    get compareToBaseProbs() {
      return Pn.value;
    },
    marginTop: 32,
    marginRight: 92,
    marginLeft: 80,
    marginBottom: 40,
    get width() {
      return l(u).width;
    },
    get height() {
      return l(u).height;
    },
    xAxisLabel: "Activation value",
    yAxisLabel: "Predicted label",
    showColorLegend: !0
  });
  var B = m(L, 2), O = b(B), X = b(O), Q = m(b(X), 2);
  Ye(Q, {
    position: "right",
    trigger: (Z) => {
      Ze(Z, {});
    },
    content: (Z) => {
      var fe = Du();
      fe.textContent = `This confusion matrix is calculated from instances that cause
                this feature to activate. Checking "Compare to whole dataset" shows
                the difference relative to the confusion matrix for all
                instances.`, I(Z, fe);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var U = m(X, 2), re = b(U), ie = m(re, 2);
  ie.textContent = "Compare to whole dataset";
  var K = m(O, 2), he = b(K);
  fl(he, {
    get cm() {
      return rt.value.cm;
    },
    get other() {
      return Bt.value.cm;
    },
    get showDifference() {
      return Rn.value;
    },
    legend: "vertical",
    get width() {
      return l(_).width;
    },
    get height() {
      return l(_).height;
    },
    marginTop: f,
    marginRight: v,
    marginBottom: c,
    marginLeft: d
  });
  var _e = m(B, 2), pe = b(_e);
  Nu(pe, {
    get tokenColor() {
      return l(r);
    }
  });
  var Le = m(_e, 2);
  {
    var je = (P) => {
      var G = Ou(), Z = b(G);
      Ru(Z, {
        get tokenColor() {
          return l(r);
        },
        get featureId() {
          return cn.value;
        }
      }), I(P, G);
    };
    le(Le, (P) => {
      Xr.value && P(je);
    });
  }
  ne(
    (P, G) => {
      C = Be(S, "", C, { width: `${l(n) + 1}em` }), de(E, `${P ?? ""} (${G ?? ""} instances)`), qe(
        R,
        1,
        Ss([
          "sae-main",
          Xr.value ? "sae-grid-inference" : "sae-grid-no-inference"
        ]),
        "svelte-1vkzfjf"
      );
    },
    [
      () => ir(rt.value.sequence_act_rate),
      () => jt(rt.value.cm.n_sequences)
    ]
  ), mr(S, () => l(a), (P) => ee(a, P)), vn(D, () => Pn.value, (P) => Pn.value = P), Qe($, "clientWidth", (P) => ee(o, P)), Qe($, "clientHeight", (P) => ee(s, P)), vn(re, () => Rn.value, (P) => Rn.value = P), Qe(K, "clientWidth", (P) => ee(g, P)), Qe(K, "clientHeight", (P) => ee(h, P)), I(e, w), xe();
}
Rt(["keydown", "click"]);
var ju = /* @__PURE__ */ te('<div class="sae-widget-container svelte-zqdrxr"><div class="sae-tabs-container svelte-zqdrxr"><!></div> <div class="sae-tab-content svelte-zqdrxr"><!></div></div>');
function Wu(e, t) {
  me(t, !0);
  let n = /* @__PURE__ */ se("overview");
  function r(g) {
    ee(n, g, !0);
  }
  function a(g) {
    cn.value = g, ee(n, "detail");
  }
  var i = ju();
  let s;
  var o = b(i), u = b(o);
  Bs(u, {
    get selectedTab() {
      return l(n);
    },
    changeTab: r
  });
  var f = m(o, 2), v = b(f);
  {
    var c = (g) => {
      Vf(g, {});
    }, d = (g, h) => {
      {
        var _ = (T) => {
          ku(T, { onClickFeature: a });
        }, w = (T) => {
          Hu(T, {});
        };
        le(
          g,
          (T) => {
            l(n) === "table" ? T(_) : T(w, !1);
          },
          h
        );
      }
    };
    le(v, (g) => {
      l(n) === "overview" ? g(c) : g(d, !1);
    });
  }
  ne(() => s = Be(i, "", s, {
    height: `${Xi.value ?? ""}px`,
    "--text-xs": `${ae.xs ?? ""}px`,
    "--text-sm": `${ae.sm ?? ""}px`,
    "--text-base": `${ae.base ?? ""}px`,
    "--text-lg": `${ae.lg ?? ""}px`,
    "--text-xl": `${ae.xl ?? ""}px`
  })), I(e, i), xe();
}
const Vu = ({ model: e, el: t }) => {
  js(e), Vs(t);
  let n = xs(Wu, { target: t });
  return () => ws(n);
}, Xu = { render: Vu };
export {
  Xu as default
};
