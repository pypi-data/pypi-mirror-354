const {
  SvelteComponent: Ze,
  add_render_callback: $e,
  append_hydration: f,
  attr: h,
  binding_callbacks: et,
  children: j,
  claim_element: k,
  claim_space: C,
  claim_text: oe,
  destroy_block: tt,
  destroy_each: Ae,
  detach: b,
  element: m,
  empty: Se,
  ensure_array_like: Le,
  get_svelte_dataset: R,
  init: lt,
  insert_hydration: O,
  listen: x,
  noop: Ie,
  run_all: je,
  safe_not_equal: st,
  select_option: xe,
  select_value: nt,
  set_data: Te,
  set_input_value: Pe,
  set_style: we,
  space: y,
  stop_propagation: it,
  text: re,
  toggle_class: Ue,
  update_keyed_each: at
} = window.__gradio__svelte__internal, { onMount: ot } = window.__gradio__svelte__internal;
function Be(n, e, l) {
  const i = n.slice();
  return i[50] = e[l], i;
}
function Me(n, e, l) {
  const i = n.slice();
  return i[50] = e[l], i;
}
function Ve(n, e, l) {
  const i = n.slice();
  return i[55] = e[l], i;
}
function Re(n) {
  let e, l = (
    /*category*/
    n[55] + ""
  ), i;
  return {
    c() {
      e = m("option"), i = re(l), this.h();
    },
    l(t) {
      e = k(t, "OPTION", {});
      var r = j(e);
      i = oe(r, l), r.forEach(b), this.h();
    },
    h() {
      e.__value = /*category*/
      n[55], Pe(e, e.__value);
    },
    m(t, r) {
      O(t, e, r), f(e, i);
    },
    p: Ie,
    d(t) {
      t && b(e);
    }
  };
}
function He(n) {
  let e, l, i;
  function t(v, s) {
    return s[0] & /*searchFilter*/
    4 && (l = null), l == null && (l = !!/*searchFilter*/
    v[2].trim()), l ? ut : rt;
  }
  let r = t(n, [-1, -1]), p = r(n);
  return {
    c() {
      e = m("div"), p.c(), i = y(), this.h();
    },
    l(v) {
      e = k(v, "DIV", { class: !0 });
      var s = j(e);
      p.l(s), i = C(s), s.forEach(b), this.h();
    },
    h() {
      h(e, "class", "no-components svelte-zk15k");
    },
    m(v, s) {
      O(v, e, s), p.m(e, null), f(e, i);
    },
    p(v, s) {
      r === (r = t(v, s)) && p ? p.p(v, s) : (p.d(1), p = r(v), p && (p.c(), p.m(e, i)));
    },
    d(v) {
      v && b(e), p.d();
    }
  };
}
function rt(n) {
  let e;
  return {
    c() {
      e = re("Loading components...");
    },
    l(l) {
      e = oe(l, "Loading components...");
    },
    m(l, i) {
      O(l, e, i);
    },
    p: Ie,
    d(l) {
      l && b(e);
    }
  };
}
function ut(n) {
  let e, l, i;
  return {
    c() {
      e = re('No components match "'), l = re(
        /*searchFilter*/
        n[2]
      ), i = re('"');
    },
    l(t) {
      e = oe(t, 'No components match "'), l = oe(
        t,
        /*searchFilter*/
        n[2]
      ), i = oe(t, '"');
    },
    m(t, r) {
      O(t, e, r), O(t, l, r), O(t, i, r);
    },
    p(t, r) {
      r[0] & /*searchFilter*/
      4 && Te(
        l,
        /*searchFilter*/
        t[2]
      );
    },
    d(t) {
      t && (b(e), b(l), b(i));
    }
  };
}
function Fe(n) {
  let e, l, i = (
    /*component*/
    n[50].icon + ""
  ), t, r, p, v = (
    /*component*/
    n[50].label + ""
  ), s, c, ee, q;
  function S(...D) {
    return (
      /*dragstart_handler*/
      n[29](
        /*component*/
        n[50],
        ...D
      )
    );
  }
  return {
    c() {
      e = m("div"), l = m("span"), t = re(i), r = y(), p = m("span"), s = re(v), c = y(), this.h();
    },
    l(D) {
      e = k(D, "DIV", { class: !0, draggable: !0 });
      var N = j(e);
      l = k(N, "SPAN", { class: !0 });
      var M = j(l);
      t = oe(M, i), M.forEach(b), r = C(N), p = k(N, "SPAN", { class: !0 });
      var g = j(p);
      s = oe(g, v), g.forEach(b), c = C(N), N.forEach(b), this.h();
    },
    h() {
      h(l, "class", "icon svelte-zk15k"), h(p, "class", "label svelte-zk15k"), h(e, "class", "palette-item svelte-zk15k"), h(e, "draggable", "true");
    },
    m(D, N) {
      O(D, e, N), f(e, l), f(l, t), f(e, r), f(e, p), f(p, s), f(e, c), ee || (q = x(e, "dragstart", S), ee = !0);
    },
    p(D, N) {
      n = D, N[0] & /*displayComponents*/
      64 && i !== (i = /*component*/
      n[50].icon + "") && Te(t, i), N[0] & /*displayComponents*/
      64 && v !== (v = /*component*/
      n[50].label + "") && Te(s, v);
    },
    d(D) {
      D && b(e), ee = !1, q();
    }
  };
}
function Ge(n, e) {
  let l, i, t, r, p = (
    /*component*/
    e[50].type + ""
  ), v, s, c, ee = "❌", q, S, D = (
    /*component*/
    (e[50].props.label || /*component*/
    e[50].props.value || "Component") + ""
  ), N, M, g, G;
  function te() {
    return (
      /*click_handler*/
      e[30](
        /*component*/
        e[50]
      )
    );
  }
  function J() {
    return (
      /*click_handler_1*/
      e[31](
        /*component*/
        e[50]
      )
    );
  }
  function Z(...I) {
    return (
      /*mousedown_handler*/
      e[32](
        /*component*/
        e[50],
        ...I
      )
    );
  }
  return {
    key: n,
    first: null,
    c() {
      l = m("div"), i = m("div"), t = m("div"), r = m("span"), v = re(p), s = y(), c = m("button"), c.textContent = ee, q = y(), S = m("span"), N = re(D), M = y(), this.h();
    },
    l(I) {
      l = k(I, "DIV", { class: !0, style: !0 });
      var T = j(l);
      i = k(T, "DIV", { class: !0 });
      var U = j(i);
      t = k(U, "DIV", { class: !0 });
      var X = j(t);
      r = k(X, "SPAN", { class: !0 });
      var W = j(r);
      v = oe(W, p), W.forEach(b), s = C(X), c = k(X, "BUTTON", {
        class: !0,
        type: !0,
        "data-svelte-h": !0
      }), R(c) !== "svelte-1dvzppr" && (c.textContent = ee), X.forEach(b), q = C(U), S = k(U, "SPAN", { class: !0 });
      var pe = j(S);
      N = oe(pe, D), pe.forEach(b), U.forEach(b), M = C(T), T.forEach(b), this.h();
    },
    h() {
      var I;
      h(r, "class", "type svelte-zk15k"), h(c, "class", "delete-btn svelte-zk15k"), h(c, "type", "button"), h(t, "class", "component-header svelte-zk15k"), h(S, "class", "label svelte-zk15k"), h(i, "class", "component-preview svelte-zk15k"), h(l, "class", "canvas-component svelte-zk15k"), we(
        l,
        "left",
        /*component*/
        e[50].position.x + "px"
      ), we(
        l,
        "top",
        /*component*/
        e[50].position.y + "px"
      ), we(
        l,
        "width",
        /*component*/
        e[50].size.width + "px"
      ), we(
        l,
        "height",
        /*component*/
        e[50].size.height + "px"
      ), Ue(
        l,
        "selected",
        /*selectedComponent*/
        ((I = e[5]) == null ? void 0 : I.id) === /*component*/
        e[50].id
      ), this.first = l;
    },
    m(I, T) {
      O(I, l, T), f(l, i), f(i, t), f(t, r), f(r, v), f(t, s), f(t, c), f(i, q), f(i, S), f(S, N), f(l, M), g || (G = [
        x(c, "click", it(te)),
        x(l, "click", J),
        x(l, "mousedown", Z)
      ], g = !0);
    },
    p(I, T) {
      var U;
      e = I, T[0] & /*value*/
      1 && p !== (p = /*component*/
      e[50].type + "") && Te(v, p), T[0] & /*value*/
      1 && D !== (D = /*component*/
      (e[50].props.label || /*component*/
      e[50].props.value || "Component") + "") && Te(N, D), T[0] & /*value*/
      1 && we(
        l,
        "left",
        /*component*/
        e[50].position.x + "px"
      ), T[0] & /*value*/
      1 && we(
        l,
        "top",
        /*component*/
        e[50].position.y + "px"
      ), T[0] & /*value*/
      1 && we(
        l,
        "width",
        /*component*/
        e[50].size.width + "px"
      ), T[0] & /*value*/
      1 && we(
        l,
        "height",
        /*component*/
        e[50].size.height + "px"
      ), T[0] & /*selectedComponent, value*/
      33 && Ue(
        l,
        "selected",
        /*selectedComponent*/
        ((U = e[5]) == null ? void 0 : U.id) === /*component*/
        e[50].id
      );
    },
    d(I) {
      I && b(l), g = !1, je(G);
    }
  };
}
function pt(n) {
  let e, l = "Select a component to edit properties", i, t, r = '<strong>How to use:</strong> <ul class="svelte-zk15k"><li class="svelte-zk15k">Drag components from the palette to the canvas</li> <li class="svelte-zk15k">Click components to select and edit them</li> <li class="svelte-zk15k">Drag components around the canvas to reposition</li> <li class="svelte-zk15k">Use the properties panel to customize</li></ul>';
  return {
    c() {
      e = m("p"), e.textContent = l, i = y(), t = m("div"), t.innerHTML = r, this.h();
    },
    l(p) {
      e = k(p, "P", { "data-svelte-h": !0 }), R(e) !== "svelte-ilodow" && (e.textContent = l), i = C(p), t = k(p, "DIV", { class: !0, "data-svelte-h": !0 }), R(t) !== "svelte-15cgtbi" && (t.innerHTML = r), this.h();
    },
    h() {
      h(t, "class", "help-text svelte-zk15k");
    },
    m(p, v) {
      O(p, e, v), O(p, i, v), O(p, t, v);
    },
    p: Ie,
    d(p) {
      p && (b(e), b(i), b(t));
    }
  };
}
function ct(n) {
  let e, l, i, t = "Type:", r, p = (
    /*selectedComponent*/
    n[5].type + ""
  ), v, s, c, ee, q, S, D = (
    /*selectedComponent*/
    n[5].id + ""
  ), N, M, g, G, te, J, Z, I, T, U, X, W = "Size & Position", pe, L, H, _e = "Width:", ke, F, fe, K, le, Ce = "Height:", Q, ie, he, se, $, Oe = "X Position:", ge, ne, me, ce, A, ae = "Y Position:", B, P, de, ye, De, o = (
    /*selectedComponent*/
    n[5].props.label !== void 0 && Je(n)
  ), d = (
    /*selectedComponent*/
    n[5].props.placeholder !== void 0 && Xe(n)
  ), u = (
    /*selectedComponent*/
    n[5].props.value !== void 0 && Ye(n)
  ), _ = (
    /*selectedComponent*/
    n[5].props.choices !== void 0 && qe(n)
  ), a = (
    /*selectedComponent*/
    n[5].props.minimum !== void 0 && We(n)
  ), E = (
    /*selectedComponent*/
    n[5].props.maximum !== void 0 && Ke(n)
  ), V = (
    /*selectedComponent*/
    n[5].props.step !== void 0 && Qe(n)
  );
  return {
    c() {
      e = m("div"), l = m("div"), i = m("strong"), i.textContent = t, r = y(), v = re(p), s = y(), c = m("br"), ee = y(), q = m("small"), S = re("ID: "), N = re(D), M = y(), o && o.c(), g = y(), d && d.c(), G = y(), u && u.c(), te = y(), _ && _.c(), J = y(), a && a.c(), Z = y(), E && E.c(), I = y(), V && V.c(), T = y(), U = m("div"), X = m("h5"), X.textContent = W, pe = y(), L = m("div"), H = m("label"), H.textContent = _e, ke = y(), F = m("input"), K = y(), le = m("label"), le.textContent = Ce, Q = y(), ie = m("input"), se = y(), $ = m("label"), $.textContent = Oe, ge = y(), ne = m("input"), ce = y(), A = m("label"), A.textContent = ae, B = y(), P = m("input"), this.h();
    },
    l(w) {
      e = k(w, "DIV", { class: !0 });
      var z = j(e);
      l = k(z, "DIV", { class: !0 });
      var ue = j(l);
      i = k(ue, "STRONG", { "data-svelte-h": !0 }), R(i) !== "svelte-1y9dw9w" && (i.textContent = t), r = C(ue), v = oe(ue, p), s = C(ue), c = k(ue, "BR", {}), ee = C(ue), q = k(ue, "SMALL", {});
      var be = j(q);
      S = oe(be, "ID: "), N = oe(be, D), be.forEach(b), ue.forEach(b), M = C(z), o && o.l(z), g = C(z), d && d.l(z), G = C(z), u && u.l(z), te = C(z), _ && _.l(z), J = C(z), a && a.l(z), Z = C(z), E && E.l(z), I = C(z), V && V.l(z), T = C(z), U = k(z, "DIV", { class: !0 });
      var ze = j(U);
      X = k(ze, "H5", { class: !0, "data-svelte-h": !0 }), R(X) !== "svelte-u9anyo" && (X.textContent = W), pe = C(ze), L = k(ze, "DIV", { class: !0 });
      var Y = j(L);
      H = k(Y, "LABEL", { class: !0, "data-svelte-h": !0 }), R(H) !== "svelte-19lukby" && (H.textContent = _e), ke = C(Y), F = k(Y, "INPUT", { type: !0, class: !0 }), K = C(Y), le = k(Y, "LABEL", { class: !0, "data-svelte-h": !0 }), R(le) !== "svelte-1ls0h4v" && (le.textContent = Ce), Q = C(Y), ie = k(Y, "INPUT", { type: !0, class: !0 }), se = C(Y), $ = k(Y, "LABEL", { class: !0, "data-svelte-h": !0 }), R($) !== "svelte-1wkby0j" && ($.textContent = Oe), ge = C(Y), ne = k(Y, "INPUT", { type: !0, class: !0 }), ce = C(Y), A = k(Y, "LABEL", { class: !0, "data-svelte-h": !0 }), R(A) !== "svelte-t7u7hk" && (A.textContent = ae), B = C(Y), P = k(Y, "INPUT", { type: !0, class: !0 }), Y.forEach(b), ze.forEach(b), z.forEach(b), this.h();
    },
    h() {
      h(l, "class", "property-header svelte-zk15k"), h(X, "class", "svelte-zk15k"), h(H, "class", "svelte-zk15k"), h(F, "type", "number"), F.value = fe = /*selectedComponent*/
      n[5].size.width, h(F, "class", "svelte-zk15k"), h(le, "class", "svelte-zk15k"), h(ie, "type", "number"), ie.value = he = /*selectedComponent*/
      n[5].size.height, h(ie, "class", "svelte-zk15k"), h($, "class", "svelte-zk15k"), h(ne, "type", "number"), ne.value = me = /*selectedComponent*/
      n[5].position.x, h(ne, "class", "svelte-zk15k"), h(A, "class", "svelte-zk15k"), h(P, "type", "number"), P.value = de = /*selectedComponent*/
      n[5].position.y, h(P, "class", "svelte-zk15k"), h(L, "class", "size-controls svelte-zk15k"), h(U, "class", "size-section svelte-zk15k"), h(e, "class", "property-group svelte-zk15k");
    },
    m(w, z) {
      O(w, e, z), f(e, l), f(l, i), f(l, r), f(l, v), f(l, s), f(l, c), f(l, ee), f(l, q), f(q, S), f(q, N), f(e, M), o && o.m(e, null), f(e, g), d && d.m(e, null), f(e, G), u && u.m(e, null), f(e, te), _ && _.m(e, null), f(e, J), a && a.m(e, null), f(e, Z), E && E.m(e, null), f(e, I), V && V.m(e, null), f(e, T), f(e, U), f(U, X), f(U, pe), f(U, L), f(L, H), f(L, ke), f(L, F), f(L, K), f(L, le), f(L, Q), f(L, ie), f(L, se), f(L, $), f(L, ge), f(L, ne), f(L, ce), f(L, A), f(L, B), f(L, P), ye || (De = [
        x(
          F,
          "input",
          /*input_handler_8*/
          n[43]
        ),
        x(
          ie,
          "input",
          /*input_handler_9*/
          n[44]
        ),
        x(
          ne,
          "input",
          /*input_handler_10*/
          n[45]
        ),
        x(
          P,
          "input",
          /*input_handler_11*/
          n[46]
        )
      ], ye = !0);
    },
    p(w, z) {
      z[0] & /*selectedComponent*/
      32 && p !== (p = /*selectedComponent*/
      w[5].type + "") && Te(v, p), z[0] & /*selectedComponent*/
      32 && D !== (D = /*selectedComponent*/
      w[5].id + "") && Te(N, D), /*selectedComponent*/
      w[5].props.label !== void 0 ? o ? o.p(w, z) : (o = Je(w), o.c(), o.m(e, g)) : o && (o.d(1), o = null), /*selectedComponent*/
      w[5].props.placeholder !== void 0 ? d ? d.p(w, z) : (d = Xe(w), d.c(), d.m(e, G)) : d && (d.d(1), d = null), /*selectedComponent*/
      w[5].props.value !== void 0 ? u ? u.p(w, z) : (u = Ye(w), u.c(), u.m(e, te)) : u && (u.d(1), u = null), /*selectedComponent*/
      w[5].props.choices !== void 0 ? _ ? _.p(w, z) : (_ = qe(w), _.c(), _.m(e, J)) : _ && (_.d(1), _ = null), /*selectedComponent*/
      w[5].props.minimum !== void 0 ? a ? a.p(w, z) : (a = We(w), a.c(), a.m(e, Z)) : a && (a.d(1), a = null), /*selectedComponent*/
      w[5].props.maximum !== void 0 ? E ? E.p(w, z) : (E = Ke(w), E.c(), E.m(e, I)) : E && (E.d(1), E = null), /*selectedComponent*/
      w[5].props.step !== void 0 ? V ? V.p(w, z) : (V = Qe(w), V.c(), V.m(e, T)) : V && (V.d(1), V = null), z[0] & /*selectedComponent*/
      32 && fe !== (fe = /*selectedComponent*/
      w[5].size.width) && F.value !== fe && (F.value = fe), z[0] & /*selectedComponent*/
      32 && he !== (he = /*selectedComponent*/
      w[5].size.height) && ie.value !== he && (ie.value = he), z[0] & /*selectedComponent*/
      32 && me !== (me = /*selectedComponent*/
      w[5].position.x) && ne.value !== me && (ne.value = me), z[0] & /*selectedComponent*/
      32 && de !== (de = /*selectedComponent*/
      w[5].position.y) && P.value !== de && (P.value = de);
    },
    d(w) {
      w && b(e), o && o.d(), d && d.d(), u && u.d(), _ && _.d(), a && a.d(), E && E.d(), V && V.d(), ye = !1, je(De);
    }
  };
}
function Je(n) {
  let e, l = "Label:", i, t, r, p, v;
  return {
    c() {
      e = m("label"), e.textContent = l, i = y(), t = m("input"), this.h();
    },
    l(s) {
      e = k(s, "LABEL", { class: !0, "data-svelte-h": !0 }), R(e) !== "svelte-1mvyv0k" && (e.textContent = l), i = C(s), t = k(s, "INPUT", {
        type: !0,
        placeholder: !0,
        class: !0
      }), this.h();
    },
    h() {
      h(e, "class", "svelte-zk15k"), h(t, "type", "text"), h(t, "placeholder", "Label"), t.value = r = /*selectedComponent*/
      n[5].props.label, h(t, "class", "svelte-zk15k");
    },
    m(s, c) {
      O(s, e, c), O(s, i, c), O(s, t, c), p || (v = x(
        t,
        "input",
        /*input_handler*/
        n[34]
      ), p = !0);
    },
    p(s, c) {
      c[0] & /*selectedComponent*/
      32 && r !== (r = /*selectedComponent*/
      s[5].props.label) && t.value !== r && (t.value = r);
    },
    d(s) {
      s && (b(e), b(i), b(t)), p = !1, v();
    }
  };
}
function Xe(n) {
  let e, l = "Placeholder:", i, t, r, p, v;
  return {
    c() {
      e = m("label"), e.textContent = l, i = y(), t = m("input"), this.h();
    },
    l(s) {
      e = k(s, "LABEL", { class: !0, "data-svelte-h": !0 }), R(e) !== "svelte-s3gzvr" && (e.textContent = l), i = C(s), t = k(s, "INPUT", {
        type: !0,
        placeholder: !0,
        class: !0
      }), this.h();
    },
    h() {
      h(e, "class", "svelte-zk15k"), h(t, "type", "text"), h(t, "placeholder", "Placeholder"), t.value = r = /*selectedComponent*/
      n[5].props.placeholder, h(t, "class", "svelte-zk15k");
    },
    m(s, c) {
      O(s, e, c), O(s, i, c), O(s, t, c), p || (v = x(
        t,
        "input",
        /*input_handler_1*/
        n[35]
      ), p = !0);
    },
    p(s, c) {
      c[0] & /*selectedComponent*/
      32 && r !== (r = /*selectedComponent*/
      s[5].props.placeholder) && t.value !== r && (t.value = r);
    },
    d(s) {
      s && (b(e), b(i), b(t)), p = !1, v();
    }
  };
}
function Ye(n) {
  let e, l = "Value:", i, t;
  function r(s, c) {
    return typeof /*selectedComponent*/
    s[5].props.value == "boolean" ? ht : typeof /*selectedComponent*/
    s[5].props.value == "number" ? ft : dt;
  }
  let p = r(n), v = p(n);
  return {
    c() {
      e = m("label"), e.textContent = l, i = y(), v.c(), t = Se(), this.h();
    },
    l(s) {
      e = k(s, "LABEL", { class: !0, "data-svelte-h": !0 }), R(e) !== "svelte-1m0lw4v" && (e.textContent = l), i = C(s), v.l(s), t = Se(), this.h();
    },
    h() {
      h(e, "class", "svelte-zk15k");
    },
    m(s, c) {
      O(s, e, c), O(s, i, c), v.m(s, c), O(s, t, c);
    },
    p(s, c) {
      p === (p = r(s)) && v ? v.p(s, c) : (v.d(1), v = p(s), v && (v.c(), v.m(t.parentNode, t)));
    },
    d(s) {
      s && (b(e), b(i), b(t)), v.d(s);
    }
  };
}
function dt(n) {
  let e, l, i, t;
  return {
    c() {
      e = m("input"), this.h();
    },
    l(r) {
      e = k(r, "INPUT", {
        type: !0,
        placeholder: !0,
        class: !0
      }), this.h();
    },
    h() {
      h(e, "type", "text"), h(e, "placeholder", "Value"), e.value = l = /*selectedComponent*/
      n[5].props.value, h(e, "class", "svelte-zk15k");
    },
    m(r, p) {
      O(r, e, p), i || (t = x(
        e,
        "input",
        /*input_handler_3*/
        n[38]
      ), i = !0);
    },
    p(r, p) {
      p[0] & /*selectedComponent*/
      32 && l !== (l = /*selectedComponent*/
      r[5].props.value) && e.value !== l && (e.value = l);
    },
    d(r) {
      r && b(e), i = !1, t();
    }
  };
}
function ft(n) {
  let e, l, i, t;
  return {
    c() {
      e = m("input"), this.h();
    },
    l(r) {
      e = k(r, "INPUT", { type: !0, class: !0 }), this.h();
    },
    h() {
      h(e, "type", "number"), e.value = l = /*selectedComponent*/
      n[5].props.value, h(e, "class", "svelte-zk15k");
    },
    m(r, p) {
      O(r, e, p), i || (t = x(
        e,
        "input",
        /*input_handler_2*/
        n[37]
      ), i = !0);
    },
    p(r, p) {
      p[0] & /*selectedComponent*/
      32 && l !== (l = /*selectedComponent*/
      r[5].props.value) && e.value !== l && (e.value = l);
    },
    d(r) {
      r && b(e), i = !1, t();
    }
  };
}
function ht(n) {
  let e, l, i, t;
  return {
    c() {
      e = m("input"), this.h();
    },
    l(r) {
      e = k(r, "INPUT", { type: !0, class: !0 }), this.h();
    },
    h() {
      h(e, "type", "checkbox"), e.checked = l = /*selectedComponent*/
      n[5].props.value, h(e, "class", "svelte-zk15k");
    },
    m(r, p) {
      O(r, e, p), i || (t = x(
        e,
        "change",
        /*change_handler*/
        n[36]
      ), i = !0);
    },
    p(r, p) {
      p[0] & /*selectedComponent*/
      32 && l !== (l = /*selectedComponent*/
      r[5].props.value) && (e.checked = l);
    },
    d(r) {
      r && b(e), i = !1, t();
    }
  };
}
function qe(n) {
  let e, l = "Choices (comma-separated):", i, t, r, p, v;
  return {
    c() {
      e = m("label"), e.textContent = l, i = y(), t = m("input"), this.h();
    },
    l(s) {
      e = k(s, "LABEL", { class: !0, "data-svelte-h": !0 }), R(e) !== "svelte-s5zbc2" && (e.textContent = l), i = C(s), t = k(s, "INPUT", {
        type: !0,
        placeholder: !0,
        class: !0
      }), this.h();
    },
    h() {
      h(e, "class", "svelte-zk15k"), h(t, "type", "text"), h(t, "placeholder", "Option 1, Option 2, Option 3"), t.value = r = Array.isArray(
        /*selectedComponent*/
        n[5].props.choices
      ) ? (
        /*selectedComponent*/
        n[5].props.choices.join(", ")
      ) : (
        /*selectedComponent*/
        n[5].props.choices
      ), h(t, "class", "svelte-zk15k");
    },
    m(s, c) {
      O(s, e, c), O(s, i, c), O(s, t, c), p || (v = x(
        t,
        "input",
        /*input_handler_4*/
        n[39]
      ), p = !0);
    },
    p(s, c) {
      c[0] & /*selectedComponent*/
      32 && r !== (r = Array.isArray(
        /*selectedComponent*/
        s[5].props.choices
      ) ? (
        /*selectedComponent*/
        s[5].props.choices.join(", ")
      ) : (
        /*selectedComponent*/
        s[5].props.choices
      )) && t.value !== r && (t.value = r);
    },
    d(s) {
      s && (b(e), b(i), b(t)), p = !1, v();
    }
  };
}
function We(n) {
  let e, l = "Minimum:", i, t, r, p, v;
  return {
    c() {
      e = m("label"), e.textContent = l, i = y(), t = m("input"), this.h();
    },
    l(s) {
      e = k(s, "LABEL", { class: !0, "data-svelte-h": !0 }), R(e) !== "svelte-v7nxz2" && (e.textContent = l), i = C(s), t = k(s, "INPUT", { type: !0, class: !0 }), this.h();
    },
    h() {
      h(e, "class", "svelte-zk15k"), h(t, "type", "number"), t.value = r = /*selectedComponent*/
      n[5].props.minimum, h(t, "class", "svelte-zk15k");
    },
    m(s, c) {
      O(s, e, c), O(s, i, c), O(s, t, c), p || (v = x(
        t,
        "input",
        /*input_handler_5*/
        n[40]
      ), p = !0);
    },
    p(s, c) {
      c[0] & /*selectedComponent*/
      32 && r !== (r = /*selectedComponent*/
      s[5].props.minimum) && t.value !== r && (t.value = r);
    },
    d(s) {
      s && (b(e), b(i), b(t)), p = !1, v();
    }
  };
}
function Ke(n) {
  let e, l = "Maximum:", i, t, r, p, v;
  return {
    c() {
      e = m("label"), e.textContent = l, i = y(), t = m("input"), this.h();
    },
    l(s) {
      e = k(s, "LABEL", { class: !0, "data-svelte-h": !0 }), R(e) !== "svelte-elhw0w" && (e.textContent = l), i = C(s), t = k(s, "INPUT", { type: !0, class: !0 }), this.h();
    },
    h() {
      h(e, "class", "svelte-zk15k"), h(t, "type", "number"), t.value = r = /*selectedComponent*/
      n[5].props.maximum, h(t, "class", "svelte-zk15k");
    },
    m(s, c) {
      O(s, e, c), O(s, i, c), O(s, t, c), p || (v = x(
        t,
        "input",
        /*input_handler_6*/
        n[41]
      ), p = !0);
    },
    p(s, c) {
      c[0] & /*selectedComponent*/
      32 && r !== (r = /*selectedComponent*/
      s[5].props.maximum) && t.value !== r && (t.value = r);
    },
    d(s) {
      s && (b(e), b(i), b(t)), p = !1, v();
    }
  };
}
function Qe(n) {
  let e, l = "Step:", i, t, r, p, v;
  return {
    c() {
      e = m("label"), e.textContent = l, i = y(), t = m("input"), this.h();
    },
    l(s) {
      e = k(s, "LABEL", { class: !0, "data-svelte-h": !0 }), R(e) !== "svelte-rqjdj4" && (e.textContent = l), i = C(s), t = k(s, "INPUT", { type: !0, class: !0 }), this.h();
    },
    h() {
      h(e, "class", "svelte-zk15k"), h(t, "type", "number"), t.value = r = /*selectedComponent*/
      n[5].props.step, h(t, "class", "svelte-zk15k");
    },
    m(s, c) {
      O(s, e, c), O(s, i, c), O(s, t, c), p || (v = x(
        t,
        "input",
        /*input_handler_7*/
        n[42]
      ), p = !0);
    },
    p(s, c) {
      c[0] & /*selectedComponent*/
      32 && r !== (r = /*selectedComponent*/
      s[5].props.step) && t.value !== r && (t.value = r);
    },
    d(s) {
      s && (b(e), b(i), b(t)), p = !1, v();
    }
  };
}
function vt(n) {
  let e, l, i, t, r = "🎨 Gradio Designer", p, v, s = (
    /*value*/
    n[0].components.length + ""
  ), c, ee, q, S, D, N = "📄 Export JSON", M, g, G = "🖼️ Export PNG", te, J, Z, I, T, U = "Components", X, W, pe, L, H, _e = "All Categories", ke, F, fe, K, le, Ce, Q = [], ie = /* @__PURE__ */ new Map(), he, se, $, Oe = "Properties", ge, ne, me, ce = Le(Object.keys(
    /*componentsByCategory*/
    n[7]
  )), A = [];
  for (let u = 0; u < ce.length; u += 1)
    A[u] = Re(Ve(n, ce, u));
  let ae = Le(
    /*displayComponents*/
    n[6]
  ), B = [];
  for (let u = 0; u < ae.length; u += 1)
    B[u] = Fe(Me(n, ae, u));
  let P = null;
  ae.length || (P = He(n));
  let de = Le(
    /*value*/
    n[0].components
  );
  const ye = (u) => (
    /*component*/
    u[50].id
  );
  for (let u = 0; u < de.length; u += 1) {
    let _ = Be(n, de, u), a = ye(_);
    ie.set(a, Q[u] = Ge(a, _));
  }
  function De(u, _) {
    return (
      /*selectedComponent*/
      u[5] ? ct : pt
    );
  }
  let o = De(n), d = o(n);
  return {
    c() {
      e = m("div"), l = m("div"), i = m("div"), t = m("h3"), t.textContent = r, p = y(), v = m("span"), c = re(s), ee = re(" components"), q = y(), S = m("div"), D = m("button"), D.textContent = N, M = y(), g = m("button"), g.textContent = G, te = y(), J = m("div"), Z = m("div"), I = m("div"), T = m("h4"), T.textContent = U, X = y(), W = m("input"), pe = y(), L = m("select"), H = m("option"), H.textContent = _e;
      for (let u = 0; u < A.length; u += 1)
        A[u].c();
      ke = y(), F = m("div");
      for (let u = 0; u < B.length; u += 1)
        B[u].c();
      P && P.c(), fe = y(), K = m("div"), le = m("div"), Ce = y();
      for (let u = 0; u < Q.length; u += 1)
        Q[u].c();
      he = y(), se = m("div"), $ = m("h4"), $.textContent = Oe, ge = y(), d.c(), this.h();
    },
    l(u) {
      e = k(u, "DIV", { class: !0, id: !0 });
      var _ = j(e);
      l = k(_, "DIV", { class: !0 });
      var a = j(l);
      i = k(a, "DIV", { class: !0 });
      var E = j(i);
      t = k(E, "H3", { class: !0, "data-svelte-h": !0 }), R(t) !== "svelte-1dsn5ql" && (t.textContent = r), p = C(E), v = k(E, "SPAN", { class: !0 });
      var V = j(v);
      c = oe(V, s), ee = oe(V, " components"), V.forEach(b), E.forEach(b), q = C(a), S = k(a, "DIV", { class: !0 });
      var w = j(S);
      D = k(w, "BUTTON", {
        class: !0,
        type: !0,
        "data-svelte-h": !0
      }), R(D) !== "svelte-1n26als" && (D.textContent = N), M = C(w), g = k(w, "BUTTON", {
        class: !0,
        type: !0,
        "data-svelte-h": !0
      }), R(g) !== "svelte-1yzlvvh" && (g.textContent = G), w.forEach(b), a.forEach(b), te = C(_), J = k(_, "DIV", { class: !0 });
      var z = j(J);
      Z = k(z, "DIV", { class: !0 });
      var ue = j(Z);
      I = k(ue, "DIV", { class: !0 });
      var be = j(I);
      T = k(be, "H4", { class: !0, "data-svelte-h": !0 }), R(T) !== "svelte-6fxyga" && (T.textContent = U), X = C(be), W = k(be, "INPUT", {
        type: !0,
        placeholder: !0,
        class: !0
      }), pe = C(be), L = k(be, "SELECT", { class: !0 });
      var ze = j(L);
      H = k(ze, "OPTION", { "data-svelte-h": !0 }), R(H) !== "svelte-1dzjcyu" && (H.textContent = _e);
      for (let ve = 0; ve < A.length; ve += 1)
        A[ve].l(ze);
      ze.forEach(b), be.forEach(b), ke = C(ue), F = k(ue, "DIV", { class: !0 });
      var Y = j(F);
      for (let ve = 0; ve < B.length; ve += 1)
        B[ve].l(Y);
      P && P.l(Y), Y.forEach(b), ue.forEach(b), fe = C(z), K = k(z, "DIV", { class: !0 });
      var Ee = j(K);
      le = k(Ee, "DIV", { class: !0 }), j(le).forEach(b), Ce = C(Ee);
      for (let ve = 0; ve < Q.length; ve += 1)
        Q[ve].l(Ee);
      Ee.forEach(b), he = C(z), se = k(z, "DIV", { class: !0 });
      var Ne = j(se);
      $ = k(Ne, "H4", { class: !0, "data-svelte-h": !0 }), R($) !== "svelte-100vz0b" && ($.textContent = Oe), ge = C(Ne), d.l(Ne), Ne.forEach(b), z.forEach(b), _.forEach(b), this.h();
    },
    h() {
      h(t, "class", "svelte-zk15k"), h(v, "class", "component-count svelte-zk15k"), h(i, "class", "toolbar-left svelte-zk15k"), h(D, "class", "export-btn svelte-zk15k"), h(D, "type", "button"), h(g, "class", "export-btn svelte-zk15k"), h(g, "type", "button"), h(S, "class", "toolbar-right svelte-zk15k"), h(l, "class", "toolbar svelte-zk15k"), h(T, "class", "svelte-zk15k"), h(W, "type", "text"), h(W, "placeholder", "Search components..."), h(W, "class", "search-input svelte-zk15k"), H.__value = "All", Pe(H, H.__value), h(L, "class", "category-select svelte-zk15k"), /*selectedCategory*/
      n[3] === void 0 && $e(() => (
        /*select_change_handler*/
        n[28].call(L)
      )), h(I, "class", "palette-header svelte-zk15k"), h(F, "class", "palette-content svelte-zk15k"), h(Z, "class", "palette svelte-zk15k"), h(le, "class", "canvas-grid svelte-zk15k"), h(K, "class", "canvas svelte-zk15k"), h($, "class", "svelte-zk15k"), h(se, "class", "properties svelte-zk15k"), h(J, "class", "designer-content svelte-zk15k"), h(e, "class", "designer-container svelte-zk15k"), h(
        e,
        "id",
        /*elem_id*/
        n[1]
      );
    },
    m(u, _) {
      O(u, e, _), f(e, l), f(l, i), f(i, t), f(i, p), f(i, v), f(v, c), f(v, ee), f(l, q), f(l, S), f(S, D), f(S, M), f(S, g), f(e, te), f(e, J), f(J, Z), f(Z, I), f(I, T), f(I, X), f(I, W), Pe(
        W,
        /*searchFilter*/
        n[2]
      ), f(I, pe), f(I, L), f(L, H);
      for (let a = 0; a < A.length; a += 1)
        A[a] && A[a].m(L, null);
      xe(
        L,
        /*selectedCategory*/
        n[3],
        !0
      ), f(Z, ke), f(Z, F);
      for (let a = 0; a < B.length; a += 1)
        B[a] && B[a].m(F, null);
      P && P.m(F, null), f(J, fe), f(J, K), f(K, le), f(K, Ce);
      for (let a = 0; a < Q.length; a += 1)
        Q[a] && Q[a].m(K, null);
      n[33](K), f(J, he), f(J, se), f(se, $), f(se, ge), d.m(se, null), ne || (me = [
        x(
          window,
          "mousemove",
          /*onCanvasMouseMove*/
          n[18]
        ),
        x(
          window,
          "mouseup",
          /*onCanvasMouseUp*/
          n[19]
        ),
        x(
          D,
          "click",
          /*exportAsJSON*/
          n[15]
        ),
        x(
          g,
          "click",
          /*exportAsPNG*/
          n[16]
        ),
        x(
          W,
          "input",
          /*input_input_handler*/
          n[27]
        ),
        x(
          L,
          "change",
          /*select_change_handler*/
          n[28]
        ),
        x(K, "dragover", _t),
        x(
          K,
          "drop",
          /*onDrop*/
          n[9]
        )
      ], ne = !0);
    },
    p(u, _) {
      if (_[0] & /*value*/
      1 && s !== (s = /*value*/
      u[0].components.length + "") && Te(c, s), _[0] & /*searchFilter*/
      4 && W.value !== /*searchFilter*/
      u[2] && Pe(
        W,
        /*searchFilter*/
        u[2]
      ), _[0] & /*componentsByCategory*/
      128) {
        ce = Le(Object.keys(
          /*componentsByCategory*/
          u[7]
        ));
        let a;
        for (a = 0; a < ce.length; a += 1) {
          const E = Ve(u, ce, a);
          A[a] ? A[a].p(E, _) : (A[a] = Re(E), A[a].c(), A[a].m(L, null));
        }
        for (; a < A.length; a += 1)
          A[a].d(1);
        A.length = ce.length;
      }
      if (_[0] & /*selectedCategory, componentsByCategory*/
      136 && xe(
        L,
        /*selectedCategory*/
        u[3]
      ), _[0] & /*onDragStart, displayComponents, searchFilter*/
      324) {
        ae = Le(
          /*displayComponents*/
          u[6]
        );
        let a;
        for (a = 0; a < ae.length; a += 1) {
          const E = Me(u, ae, a);
          B[a] ? B[a].p(E, _) : (B[a] = Fe(E), B[a].c(), B[a].m(F, null));
        }
        for (; a < B.length; a += 1)
          B[a].d(1);
        B.length = ae.length, !ae.length && P ? P.p(u, _) : ae.length ? P && (P.d(1), P = null) : (P = He(u), P.c(), P.m(F, null));
      }
      _[0] & /*value, selectedComponent, selectComponent, onComponentMouseDown, deleteComponent*/
      148513 && (de = Le(
        /*value*/
        u[0].components
      ), Q = at(Q, _, ye, 1, u, de, ie, K, tt, Ge, null, Be)), o === (o = De(u)) && d ? d.p(u, _) : (d.d(1), d = o(u), d && (d.c(), d.m(se, null))), _[0] & /*elem_id*/
      2 && h(
        e,
        "id",
        /*elem_id*/
        u[1]
      );
    },
    i: Ie,
    o: Ie,
    d(u) {
      u && b(e), Ae(A, u), Ae(B, u), P && P.d();
      for (let _ = 0; _ < Q.length; _ += 1)
        Q[_].d();
      n[33](null), d.d(), ne = !1, je(me);
    }
  };
}
function _t(n) {
  n.preventDefault(), n.dataTransfer && (n.dataTransfer.dropEffect = "copy");
}
function kt(n) {
  return {
    Textbox: {
      label: "Text Input",
      placeholder: "Enter text...",
      value: ""
    },
    TextArea: {
      label: "Text Area",
      placeholder: "Enter multiple lines...",
      lines: 3,
      value: ""
    },
    Button: {
      value: "Click me",
      variant: "secondary",
      size: "sm"
    },
    Slider: {
      label: "Slider",
      minimum: 0,
      maximum: 100,
      step: 1,
      value: 50
    },
    Number: { label: "Number", value: 0, precision: 0 },
    Checkbox: { label: "Checkbox", value: !1 },
    CheckboxGroup: {
      label: "Checkbox Group",
      choices: ["Option 1", "Option 2"],
      value: []
    },
    Radio: {
      label: "Radio",
      choices: ["Option 1", "Option 2"],
      value: "Option 1"
    },
    Dropdown: {
      label: "Dropdown",
      choices: ["Option 1", "Option 2"],
      value: "Option 1",
      multiselect: !1
    },
    Toggle: { label: "Toggle", value: !1 },
    ColorPicker: { label: "Color Picker", value: "#ff0000" },
    Date: { label: "Date", value: "2025-01-01" },
    Time: { label: "Time", value: "12:00" },
    File: {
      label: "Upload File",
      file_types: [".txt", ".pdf"]
    },
    Image: {
      label: "Image",
      type: "pil",
      interactive: !0
    },
    Video: { label: "Video", format: "mp4" },
    Audio: { label: "Audio" },
    Dataframe: {
      headers: ["Column 1", "Column 2"],
      datatype: ["str", "str"],
      value: []
    },
    JSON: { value: "{}" },
    Markdown: { value: "# Markdown Text" },
    HTML: { value: "<p>HTML Content</p>" },
    Label: { value: "Label Text" },
    Progress: { value: 0.5 }
  }[n] || {};
}
function mt(n, e, l) {
  let i, t, r, { gradio: p } = e, { elem_id: v = "" } = e;
  const s = [];
  let { value: c = { components: [], layout: "blocks" } } = e;
  const ee = void 0, q = "interactive", S = {
    Input: [
      {
        type: "Textbox",
        label: "Text Input",
        icon: "📝"
      },
      {
        type: "TextArea",
        label: "Text Area",
        icon: "📄"
      },
      {
        type: "Number",
        label: "Number",
        icon: "🔢"
      },
      {
        type: "Slider",
        label: "Slider",
        icon: "🎚️"
      },
      {
        type: "Checkbox",
        label: "Checkbox",
        icon: "☑️"
      },
      {
        type: "CheckboxGroup",
        label: "Checkbox Group",
        icon: "☑️"
      },
      {
        type: "Radio",
        label: "Radio",
        icon: "🔘"
      },
      {
        type: "Dropdown",
        label: "Dropdown",
        icon: "📋"
      },
      {
        type: "Toggle",
        label: "Toggle",
        icon: "🔄"
      },
      {
        type: "ColorPicker",
        label: "Color Picker",
        icon: "🎨"
      },
      { type: "Date", label: "Date", icon: "📅" },
      { type: "Time", label: "Time", icon: "⏰" },
      {
        type: "File",
        label: "File Upload",
        icon: "📁"
      }
    ],
    Action: [
      {
        type: "Button",
        label: "Button",
        icon: "🔘"
      }
    ],
    Media: [
      {
        type: "Image",
        label: "Image",
        icon: "🖼️"
      },
      {
        type: "Video",
        label: "Video",
        icon: "🎥"
      },
      {
        type: "Audio",
        label: "Audio",
        icon: "🎵"
      }
    ],
    Data: [
      {
        type: "Dataframe",
        label: "Dataframe",
        icon: "📊"
      },
      { type: "JSON", label: "JSON", icon: "📋" }
    ],
    Display: [
      {
        type: "Markdown",
        label: "Markdown",
        icon: "📝"
      },
      { type: "HTML", label: "HTML", icon: "🌐" },
      {
        type: "Label",
        label: "Label",
        icon: "🏷️"
      },
      {
        type: "Progress",
        label: "Progress",
        icon: "📈"
      }
    ]
  };
  let D = !1;
  ot(() => {
    l(24, D = !0);
  });
  let N = null, M, g = null, G = "", te = "All";
  function J(o, d) {
    N = d, o.dataTransfer && (o.dataTransfer.effectAllowed = "copy");
  }
  function Z(o) {
    if (o.preventDefault(), !N) return;
    const d = M.getBoundingClientRect(), u = o.clientX - d.left, _ = o.clientY - d.top, a = {
      id: `${N.type.toLowerCase()}_${Date.now()}`,
      type: N.type,
      position: { x: u, y: _ },
      size: { width: 200, height: 100 },
      props: kt(N.type)
    };
    l(0, c = Object.assign(Object.assign({}, c), {
      components: [...c.components, a]
    })), p.dispatch("change", c), N = null;
  }
  function I(o) {
    l(5, g = o);
  }
  function T(o, d) {
    if (!g) return;
    o === "choices" && typeof d == "string" ? d = d.split(",").map((_) => _.trim()).filter((_) => _) : o === "file_types" && typeof d == "string" && (d = d.split(",").map((_) => _.trim()).filter((_) => _));
    const u = c.components.map((_) => _.id === g.id ? Object.assign(Object.assign({}, _), {
      props: Object.assign(Object.assign({}, _.props), { [o]: d })
    }) : _);
    l(5, g = Object.assign(Object.assign({}, g), {
      props: Object.assign(Object.assign({}, g.props), { [o]: d })
    })), l(0, c = Object.assign(Object.assign({}, c), { components: u })), p.dispatch("change", c);
  }
  function U(o, d, u) {
    const _ = c.components.map((a) => a.id === o.id ? Object.assign(Object.assign({}, a), { position: { x: d, y: u } }) : a);
    l(0, c = Object.assign(Object.assign({}, c), { components: _ })), p.dispatch("change", c);
  }
  function X(o, d, u) {
    const _ = c.components.map((a) => a.id === o.id ? Object.assign(Object.assign({}, a), {
      size: { width: d, height: u }
    }) : a);
    (g == null ? void 0 : g.id) === o.id && l(5, g = Object.assign(Object.assign({}, g), {
      size: { width: d, height: u }
    })), l(0, c = Object.assign(Object.assign({}, c), { components: _ })), p.dispatch("change", c);
  }
  function W(o) {
    const d = c.components.filter((u) => u.id !== o);
    l(0, c = Object.assign(Object.assign({}, c), { components: d })), l(5, g = null), p.dispatch("change", c);
  }
  function pe() {
    const o = Object.assign(Object.assign({}, c), {
      metadata: {
        version: "1.0",
        created_at: (/* @__PURE__ */ new Date()).toISOString(),
        app_type: "gradio_interface",
        component_count: c.components.length
      }
    }), d = JSON.stringify(o, null, 2), u = new Blob([d], { type: "application/json" }), _ = URL.createObjectURL(u), a = document.createElement("a");
    a.href = _, a.download = "gradio-design.json", a.click(), URL.revokeObjectURL(_);
  }
  function L() {
    try {
      const o = document.createElement("canvas"), d = o.getContext("2d"), u = M.getBoundingClientRect();
      o.width = u.width * 2, o.height = u.height * 2, d.scale(2, 2), d.fillStyle = "#ffffff", d.fillRect(0, 0, u.width, u.height), d.strokeStyle = "rgba(0,0,0,0.1)", d.lineWidth = 1;
      for (let a = 0; a <= u.width; a += 20)
        d.moveTo(a, 0), d.lineTo(a, u.height);
      for (let a = 0; a <= u.height; a += 20)
        d.moveTo(0, a), d.lineTo(u.width, a);
      d.stroke(), c.components.forEach((a) => {
        const E = i.find((V) => V.type === a.type);
        d.fillStyle = "#ffffff", d.strokeStyle = "#ddd", d.lineWidth = 2, d.fillRect(a.position.x, a.position.y, a.size.width, a.size.height), d.strokeRect(a.position.x, a.position.y, a.size.width, a.size.height), d.fillStyle = "#333", d.font = "16px Arial", d.textAlign = "center", d.fillText(
          (E == null ? void 0 : E.icon) || "📦",
          a.position.x + a.size.width / 2,
          a.position.y + 25
        ), d.font = "12px Arial", d.fillText(a.type, a.position.x + a.size.width / 2, a.position.y + a.size.height / 2), d.fillText(a.props.label || a.props.value || "", a.position.x + a.size.width / 2, a.position.y + a.size.height / 2 + 15);
      });
      const _ = document.createElement("a");
      _.download = "gradio-design.png", _.href = o.toDataURL("image/png"), _.click();
    } catch (o) {
      console.error("Canvas export failed:", o), alert("PNG export failed. Check console for details.");
    }
  }
  let H = !1, _e = { x: 0, y: 0 };
  function ke(o, d) {
    if (o.button !== 0) return;
    H = !0, l(5, g = d);
    const u = M.getBoundingClientRect();
    _e.x = o.clientX - u.left - d.position.x, _e.y = o.clientY - u.top - d.position.y, o.preventDefault();
  }
  function F(o) {
    if (!H || !g) return;
    const d = M.getBoundingClientRect(), u = o.clientX - d.left - _e.x, _ = o.clientY - d.top - _e.y;
    U(g, Math.max(0, u), Math.max(0, _));
  }
  function fe() {
    H = !1;
  }
  function K() {
    G = this.value, l(2, G);
  }
  function le() {
    te = nt(this), l(3, te), l(7, S);
  }
  const Ce = (o, d) => J(d, o), Q = (o) => W(o.id), ie = (o) => I(o), he = (o, d) => ke(d, o);
  function se(o) {
    et[o ? "unshift" : "push"](() => {
      M = o, l(4, M);
    });
  }
  const $ = (o) => T("label", o.target.value), Oe = (o) => T("placeholder", o.target.value), ge = (o) => T("value", o.target.checked), ne = (o) => T("value", parseFloat(o.target.value) || 0), me = (o) => T("value", o.target.value), ce = (o) => T("choices", o.target.value), A = (o) => T("minimum", parseFloat(o.target.value) || 0), ae = (o) => T("maximum", parseFloat(o.target.value) || 100), B = (o) => T("step", parseFloat(o.target.value) || 1), P = (o) => X(g, parseInt(o.target.value) || 200, g.size.height), de = (o) => X(g, g.size.width, parseInt(o.target.value) || 100), ye = (o) => U(g, parseInt(o.target.value) || 0, g.position.y), De = (o) => U(g, g.position.x, parseInt(o.target.value) || 0);
  return n.$$set = (o) => {
    "gradio" in o && l(20, p = o.gradio), "elem_id" in o && l(1, v = o.elem_id), "value" in o && l(0, c = o.value);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*selectedCategory, allComponents, searchFilter*/
    33554444 && l(26, t = (() => {
      if (te === "All") {
        let o = i;
        return G.trim() ? o.filter((d) => d.type.toLowerCase().includes(G.toLowerCase()) || d.label.toLowerCase().includes(G.toLowerCase())) : o;
      } else {
        let o = S[te] || [];
        return G.trim() ? o.filter((d) => d.type.toLowerCase().includes(G.toLowerCase()) || d.label.toLowerCase().includes(G.toLowerCase())) : o;
      }
    })()), n.$$.dirty[0] & /*mounted, filteredComponents, allComponents*/
    117440512 && l(6, r = D ? t : i);
  }, l(25, i = Object.values(S).flat()), [
    c,
    v,
    G,
    te,
    M,
    g,
    r,
    S,
    J,
    Z,
    I,
    T,
    U,
    X,
    W,
    pe,
    L,
    ke,
    F,
    fe,
    p,
    s,
    ee,
    q,
    D,
    i,
    t,
    K,
    le,
    Ce,
    Q,
    ie,
    he,
    se,
    $,
    Oe,
    ge,
    ne,
    me,
    ce,
    A,
    ae,
    B,
    P,
    de,
    ye,
    De
  ];
}
class bt extends Ze {
  constructor(e) {
    super(), lt(
      this,
      e,
      mt,
      vt,
      st,
      {
        gradio: 20,
        elem_id: 1,
        elem_classes: 21,
        value: 0,
        loading_status: 22,
        mode: 23
      },
      null,
      [-1, -1]
    );
  }
  get elem_classes() {
    return this.$$.ctx[21];
  }
  get loading_status() {
    return this.$$.ctx[22];
  }
  get mode() {
    return this.$$.ctx[23];
  }
}
export {
  bt as default
};
