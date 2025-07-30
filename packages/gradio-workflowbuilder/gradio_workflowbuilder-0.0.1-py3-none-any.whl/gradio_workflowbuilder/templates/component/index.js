const {
  SvelteComponent: ll,
  append_hydration: y,
  attr: i,
  binding_callbacks: It,
  bubble: rt,
  children: P,
  claim_element: b,
  claim_space: R,
  claim_svg_element: Fe,
  claim_text: U,
  destroy_block: Pt,
  destroy_each: Ke,
  detach: m,
  element: k,
  empty: de,
  ensure_array_like: le,
  get_svelte_dataset: ke,
  init: al,
  insert_hydration: N,
  listen: T,
  noop: vt,
  run_all: Pe,
  safe_not_equal: nl,
  select_option: gt,
  set_data: ce,
  set_input_value: $e,
  set_style: X,
  space: Y,
  stop_propagation: Te,
  svg_element: Ve,
  text: G,
  toggle_class: Se,
  update_keyed_each: Et
} = window.__gradio__svelte__internal, { createEventDispatcher: sl, onMount: ol } = window.__gradio__svelte__internal;
function Dt(t, e, l) {
  const a = t.slice();
  return a[90] = e[l], a;
}
function Mt(t, e, l) {
  const a = t.slice();
  return a[93] = e[l], a;
}
function Nt(t, e, l) {
  const a = t.slice();
  a[96] = e[l];
  const n = (
    /*getComponentConfig*/
    a[36](
      /*node*/
      a[96].type
    )
  );
  return a[97] = n, a;
}
function Ct(t, e, l) {
  const a = t.slice();
  return a[103] = e[l][0], a[104] = e[l][1], a[106] = l, a;
}
function il(t) {
  const e = t.slice(), l = Object.entries(
    /*node*/
    e[96].data.template
  ).filter(([o, s]) => s.is_handle);
  e[100] = l;
  const a = (
    /*templateHandles*/
    e[100].some(([o, s]) => s.type === "object")
  );
  e[101] = a;
  const n = (
    /*templateHandles*/
    e[100].some(([o, s]) => s.type === "string" || s.type === "list" || s.type === "file")
  );
  return e[102] = n, e;
}
function At(t, e, l) {
  const a = t.slice();
  return a[90] = e[l], a;
}
function St(t, e, l) {
  const a = t.slice();
  return a[93] = e[l], a;
}
function bt(t) {
  const e = t.slice(), l = (
    /*nodes*/
    e[4].find((a) => a.id === /*connectionStart*/
    e[9])
  );
  return e[111] = l, e;
}
function Tt(t, e, l) {
  const a = t.slice();
  a[112] = e[l];
  const n = (
    /*nodes*/
    a[4].find(function(...p) {
      return (
        /*func*/
        t[50](
          /*edge*/
          a[112],
          ...p
        )
      );
    })
  );
  a[113] = n;
  const o = (
    /*nodes*/
    a[4].find(function(...p) {
      return (
        /*func_1*/
        t[51](
          /*edge*/
          a[112],
          ...p
        )
      );
    })
  );
  return a[114] = o, a;
}
function kt(t) {
  const e = t.slice(), l = El(
    /*sourceNode*/
    e[113],
    /*targetNode*/
    e[114]
  );
  return e[117] = l, e;
}
function Ot(t, e, l) {
  const a = t.slice();
  return a[118] = e[l][0], a[119] = e[l][1], a;
}
function Rt(t, e, l) {
  const a = t.slice();
  return a[122] = e[l][0], a[123] = e[l][1], a;
}
function Yt(t) {
  let e, l = "Components";
  return {
    c() {
      e = k("h3"), e.textContent = l, this.h();
    },
    l(a) {
      e = b(a, "H3", { class: !0, "data-svelte-h": !0 }), ke(e) !== "svelte-zv3r40" && (e.textContent = l), this.h();
    },
    h() {
      i(e, "class", "svelte-c4syt2");
    },
    m(a, n) {
      N(a, e, n);
    },
    d(a) {
      a && m(e);
    }
  };
}
function Lt(t) {
  let e, l = le(Object.entries(
    /*componentCategories*/
    t[17]
  )), a = [];
  for (let n = 0; n < l.length; n += 1)
    a[n] = Vt(Ot(t, l, n));
  return {
    c() {
      e = k("div");
      for (let n = 0; n < a.length; n += 1)
        a[n].c();
      this.h();
    },
    l(n) {
      e = b(n, "DIV", { class: !0 });
      var o = P(e);
      for (let s = 0; s < a.length; s += 1)
        a[s].l(o);
      o.forEach(m), this.h();
    },
    h() {
      i(e, "class", "sidebar-content svelte-c4syt2");
    },
    m(n, o) {
      N(n, e, o);
      for (let s = 0; s < a.length; s += 1)
        a[s] && a[s].m(e, null);
    },
    p(n, o) {
      if (o[0] & /*componentCategories, handleSidebarDragStart*/
      33685504) {
        l = le(Object.entries(
          /*componentCategories*/
          n[17]
        ));
        let s;
        for (s = 0; s < l.length; s += 1) {
          const p = Ot(n, l, s);
          a[s] ? a[s].p(p, o) : (a[s] = Vt(p), a[s].c(), a[s].m(e, null));
        }
        for (; s < a.length; s += 1)
          a[s].d(1);
        a.length = l.length;
      }
    },
    d(n) {
      n && m(e), Ke(a, n);
    }
  };
}
function Ft(t) {
  let e, l, a = (
    /*component*/
    t[123].icon + ""
  ), n, o, s, p = (
    /*component*/
    t[123].label + ""
  ), u, d, c, _;
  function v(...g) {
    return (
      /*dragstart_handler*/
      t[46](
        /*componentType*/
        t[122],
        /*component*/
        t[123],
        ...g
      )
    );
  }
  return {
    c() {
      e = k("div"), l = k("span"), n = G(a), o = Y(), s = k("span"), u = G(p), d = Y(), this.h();
    },
    l(g) {
      e = b(g, "DIV", { class: !0, draggable: !0 });
      var h = P(e);
      l = b(h, "SPAN", { class: !0 });
      var I = P(l);
      n = U(I, a), I.forEach(m), o = R(h), s = b(h, "SPAN", { class: !0 });
      var E = P(s);
      u = U(E, p), E.forEach(m), d = R(h), h.forEach(m), this.h();
    },
    h() {
      i(l, "class", "component-icon svelte-c4syt2"), i(s, "class", "component-label svelte-c4syt2"), i(e, "class", "component-item svelte-c4syt2"), i(e, "draggable", "true");
    },
    m(g, h) {
      N(g, e, h), y(e, l), y(l, n), y(e, o), y(e, s), y(s, u), y(e, d), c || (_ = T(e, "dragstart", v), c = !0);
    },
    p(g, h) {
      t = g;
    },
    d(g) {
      g && m(e), c = !1, _();
    }
  };
}
function Vt(t) {
  let e, l, a, n = (
    /*category*/
    t[119].icon + ""
  ), o, s, p, u = (
    /*categoryName*/
    t[118] + ""
  ), d, c, _, v, g = le(Object.entries(
    /*category*/
    t[119].components
  )), h = [];
  for (let I = 0; I < g.length; I += 1)
    h[I] = Ft(Rt(t, g, I));
  return {
    c() {
      e = k("div"), l = k("div"), a = k("span"), o = G(n), s = Y(), p = k("span"), d = G(u), c = Y(), _ = k("div");
      for (let I = 0; I < h.length; I += 1)
        h[I].c();
      v = Y(), this.h();
    },
    l(I) {
      e = b(I, "DIV", { class: !0 });
      var E = P(e);
      l = b(E, "DIV", { class: !0 });
      var D = P(l);
      a = b(D, "SPAN", { class: !0 });
      var A = P(a);
      o = U(A, n), A.forEach(m), s = R(D), p = b(D, "SPAN", { class: !0 });
      var C = P(p);
      d = U(C, u), C.forEach(m), D.forEach(m), c = R(E), _ = b(E, "DIV", { class: !0 });
      var oe = P(_);
      for (let Q = 0; Q < h.length; Q += 1)
        h[Q].l(oe);
      oe.forEach(m), v = R(E), E.forEach(m), this.h();
    },
    h() {
      i(a, "class", "category-icon svelte-c4syt2"), i(p, "class", "category-name"), i(l, "class", "category-header svelte-c4syt2"), i(_, "class", "category-components"), i(e, "class", "category svelte-c4syt2");
    },
    m(I, E) {
      N(I, e, E), y(e, l), y(l, a), y(a, o), y(l, s), y(l, p), y(p, d), y(e, c), y(e, _);
      for (let D = 0; D < h.length; D += 1)
        h[D] && h[D].m(_, null);
      y(e, v);
    },
    p(I, E) {
      if (E[0] & /*handleSidebarDragStart, componentCategories*/
      33685504) {
        g = le(Object.entries(
          /*category*/
          I[119].components
        ));
        let D;
        for (D = 0; D < g.length; D += 1) {
          const A = Rt(I, g, D);
          h[D] ? h[D].p(A, E) : (h[D] = Ft(A), h[D].c(), h[D].m(_, null));
        }
        for (; D < h.length; D += 1)
          h[D].d(1);
        h.length = g.length;
      }
    },
    d(I) {
      I && m(e), Ke(h, I);
    }
  };
}
function Kt(t) {
  let e, l, a, n, o, s, p, u, d, c, _, v, g, h, I;
  function E() {
    return (
      /*click_handler_5*/
      t[48](
        /*edge*/
        t[112]
      )
    );
  }
  function D() {
    return (
      /*click_handler_6*/
      t[49](
        /*edge*/
        t[112]
      )
    );
  }
  return {
    c() {
      e = Ve("g"), l = Ve("path"), n = Ve("circle"), p = Ve("circle"), c = Ve("text"), _ = G(`✕
									`), this.h();
    },
    l(A) {
      e = Fe(A, "g", { class: !0 });
      var C = P(e);
      l = Fe(C, "path", {
        d: !0,
        stroke: !0,
        "stroke-width": !0,
        fill: !0,
        class: !0
      }), P(l).forEach(m), n = Fe(C, "circle", { cx: !0, cy: !0, r: !0, fill: !0 }), P(n).forEach(m), p = Fe(C, "circle", {
        cx: !0,
        cy: !0,
        r: !0,
        fill: !0,
        class: !0
      }), P(p).forEach(m), c = Fe(C, "text", {
        x: !0,
        y: !0,
        "text-anchor": !0,
        class: !0
      });
      var oe = P(c);
      _ = U(oe, `✕
									`), oe.forEach(m), C.forEach(m), this.h();
    },
    h() {
      i(l, "d", a = "M " + /*points*/
      t[117].sourceX + " " + /*points*/
      t[117].sourceY + " C " + /*points*/
      (t[117].sourceX + 80) + " " + /*points*/
      t[117].sourceY + " " + /*points*/
      (t[117].targetX - 80) + " " + /*points*/
      t[117].targetY + " " + /*points*/
      t[117].targetX + " " + /*points*/
      t[117].targetY), i(l, "stroke", "#64748b"), i(l, "stroke-width", "2"), i(l, "fill", "none"), i(l, "class", "edge-path"), i(n, "cx", o = /*points*/
      t[117].targetX), i(n, "cy", s = /*points*/
      t[117].targetY), i(n, "r", "4"), i(n, "fill", "#64748b"), i(p, "cx", u = /*points*/
      (t[117].sourceX + /*points*/
      t[117].targetX) / 2), i(p, "cy", d = /*points*/
      (t[117].sourceY + /*points*/
      t[117].targetY) / 2), i(p, "r", "10"), i(p, "fill", "#ef4444"), i(p, "class", "edge-delete svelte-c4syt2"), i(c, "x", v = /*points*/
      (t[117].sourceX + /*points*/
      t[117].targetX) / 2), i(c, "y", g = /*points*/
      (t[117].sourceY + /*points*/
      t[117].targetY) / 2 + 4), i(c, "text-anchor", "middle"), i(c, "class", "edge-delete-text svelte-c4syt2"), i(e, "class", "edge-group");
    },
    m(A, C) {
      N(A, e, C), y(e, l), y(e, n), y(e, p), y(e, c), y(c, _), h || (I = [
        T(p, "click", Te(E)),
        T(c, "click", Te(D))
      ], h = !0);
    },
    p(A, C) {
      t = A, C[0] & /*nodes, edges, propertyFields*/
      262192 && a !== (a = "M " + /*points*/
      t[117].sourceX + " " + /*points*/
      t[117].sourceY + " C " + /*points*/
      (t[117].sourceX + 80) + " " + /*points*/
      t[117].sourceY + " " + /*points*/
      (t[117].targetX - 80) + " " + /*points*/
      t[117].targetY + " " + /*points*/
      t[117].targetX + " " + /*points*/
      t[117].targetY) && i(l, "d", a), C[0] & /*nodes, edges, propertyFields*/
      262192 && o !== (o = /*points*/
      t[117].targetX) && i(n, "cx", o), C[0] & /*nodes, edges, propertyFields*/
      262192 && s !== (s = /*points*/
      t[117].targetY) && i(n, "cy", s), C[0] & /*nodes, edges, propertyFields*/
      262192 && u !== (u = /*points*/
      (t[117].sourceX + /*points*/
      t[117].targetX) / 2) && i(p, "cx", u), C[0] & /*nodes, edges, propertyFields*/
      262192 && d !== (d = /*points*/
      (t[117].sourceY + /*points*/
      t[117].targetY) / 2) && i(p, "cy", d), C[0] & /*nodes, edges, propertyFields*/
      262192 && v !== (v = /*points*/
      (t[117].sourceX + /*points*/
      t[117].targetX) / 2) && i(c, "x", v), C[0] & /*nodes, edges, propertyFields*/
      262192 && g !== (g = /*points*/
      (t[117].sourceY + /*points*/
      t[117].targetY) / 2 + 4) && i(c, "y", g);
    },
    d(A) {
      A && m(e), h = !1, Pe(I);
    }
  };
}
function jt(t, e) {
  let l, a, n = (
    /*sourceNode*/
    e[113] && /*targetNode*/
    e[114] && Kt(kt(e))
  );
  return {
    key: t,
    first: null,
    c() {
      l = de(), n && n.c(), a = de(), this.h();
    },
    l(o) {
      l = de(), n && n.l(o), a = de(), this.h();
    },
    h() {
      this.first = l;
    },
    m(o, s) {
      N(o, l, s), n && n.m(o, s), N(o, a, s);
    },
    p(o, s) {
      e = o, /*sourceNode*/
      e[113] && /*targetNode*/
      e[114] ? n ? n.p(kt(e), s) : (n = Kt(kt(e)), n.c(), n.m(a.parentNode, a)) : n && (n.d(1), n = null);
    },
    d(o) {
      o && (m(l), m(a)), n && n.d(o);
    }
  };
}
function Bt(t) {
  let e, l = (
    /*startNode*/
    t[111] && Ht(t)
  );
  return {
    c() {
      l && l.c(), e = de();
    },
    l(a) {
      l && l.l(a), e = de();
    },
    m(a, n) {
      l && l.m(a, n), N(a, e, n);
    },
    p(a, n) {
      /*startNode*/
      a[111] ? l ? l.p(a, n) : (l = Ht(a), l.c(), l.m(e.parentNode, e)) : l && (l.d(1), l = null);
    },
    d(a) {
      a && m(e), l && l.d(a);
    }
  };
}
function Ht(t) {
  let e, l;
  return {
    c() {
      e = Ve("path"), this.h();
    },
    l(a) {
      e = Fe(a, "path", {
        d: !0,
        stroke: !0,
        "stroke-width": !0,
        "stroke-dasharray": !0,
        fill: !0,
        opacity: !0
      }), P(e).forEach(m), this.h();
    },
    h() {
      i(e, "d", l = "M " + /*startNode*/
      (t[111].position.x + 320) + " " + /*startNode*/
      (t[111].position.y + 80) + " L " + /*mousePos*/
      t[10].x + " " + /*mousePos*/
      t[10].y), i(e, "stroke", "#3b82f6"), i(e, "stroke-width", "3"), i(e, "stroke-dasharray", "8,4"), i(e, "fill", "none"), i(e, "opacity", "0.8");
    },
    m(a, n) {
      N(a, e, n);
    },
    p(a, n) {
      n[0] & /*nodes, connectionStart, mousePos, propertyFields*/
      263696 && l !== (l = "M " + /*startNode*/
      (a[111].position.x + 320) + " " + /*startNode*/
      (a[111].position.y + 80) + " L " + /*mousePos*/
      a[10].x + " " + /*mousePos*/
      a[10].y) && i(e, "d", l);
    },
    d(a) {
      a && m(e);
    }
  };
}
function rl(t) {
  let e, l = "Ready";
  return {
    c() {
      e = k("div"), e.textContent = l, this.h();
    },
    l(a) {
      e = b(a, "DIV", { class: !0, "data-svelte-h": !0 }), ke(e) !== "svelte-1jdx31r" && (e.textContent = l), this.h();
    },
    h() {
      i(e, "class", "node-status svelte-c4syt2");
    },
    m(a, n) {
      N(a, e, n);
    },
    p: vt,
    d(a) {
      a && m(e);
    }
  };
}
function pl(t) {
  let e, l = le(
    /*propertyFields*/
    t[18][
      /*node*/
      t[96].type
    ].slice(0, 3)
  ), a = [];
  for (let n = 0; n < l.length; n += 1)
    a[n] = Xt(At(t, l, n));
  return {
    c() {
      for (let n = 0; n < a.length; n += 1)
        a[n].c();
      e = de();
    },
    l(n) {
      for (let o = 0; o < a.length; o += 1)
        a[o].l(n);
      e = de();
    },
    m(n, o) {
      for (let s = 0; s < a.length; s += 1)
        a[s] && a[s].m(n, o);
      N(n, e, o);
    },
    p(n, o) {
      if (o[0] & /*nodes, propertyFields*/
      262160 | o[1] & /*updateNodeProperty*/
      4) {
        l = le(
          /*propertyFields*/
          n[18][
            /*node*/
            n[96].type
          ].slice(0, 3)
        );
        let s;
        for (s = 0; s < l.length; s += 1) {
          const p = At(n, l, s);
          a[s] ? a[s].p(p, o) : (a[s] = Xt(p), a[s].c(), a[s].m(e.parentNode, e));
        }
        for (; s < a.length; s += 1)
          a[s].d(1);
        a.length = l.length;
      }
    },
    d(n) {
      n && m(e), Ke(a, n);
    }
  };
}
function ul(t) {
  let e, l, a, n;
  function o(...s) {
    return (
      /*input_handler_2*/
      t[57](
        /*node*/
        t[96],
        /*field*/
        t[90],
        ...s
      )
    );
  }
  return {
    c() {
      e = k("input"), this.h();
    },
    l(s) {
      e = b(s, "INPUT", { class: !0, type: !0 }), this.h();
    },
    h() {
      i(e, "class", "property-input svelte-c4syt2"), i(e, "type", "text"), e.value = l = W(
        /*node*/
        t[96],
        /*field*/
        t[90].key
      ) || "";
    },
    m(s, p) {
      N(s, e, p), a || (n = [
        T(e, "input", o),
        T(e, "click", Te(
          /*click_handler_4*/
          t[45]
        ))
      ], a = !0);
    },
    p(s, p) {
      t = s, p[0] & /*nodes, propertyFields*/
      262160 && l !== (l = W(
        /*node*/
        t[96],
        /*field*/
        t[90].key
      ) || "") && e.value !== l && (e.value = l);
    },
    d(s) {
      s && m(e), a = !1, Pe(n);
    }
  };
}
function cl(t) {
  let e, l, a, n;
  function o(...s) {
    return (
      /*input_handler_1*/
      t[56](
        /*node*/
        t[96],
        /*field*/
        t[90],
        ...s
      )
    );
  }
  return {
    c() {
      e = k("textarea"), this.h();
    },
    l(s) {
      e = b(s, "TEXTAREA", { class: !0, rows: !0 }), P(e).forEach(m), this.h();
    },
    h() {
      i(e, "class", "property-input svelte-c4syt2"), e.value = l = W(
        /*node*/
        t[96],
        /*field*/
        t[90].key
      ) || "", i(e, "rows", "2");
    },
    m(s, p) {
      N(s, e, p), a || (n = [
        T(e, "input", o),
        T(e, "click", Te(
          /*click_handler_3*/
          t[44]
        ))
      ], a = !0);
    },
    p(s, p) {
      t = s, p[0] & /*nodes, propertyFields*/
      262160 && l !== (l = W(
        /*node*/
        t[96],
        /*field*/
        t[90].key
      ) || "") && (e.value = l);
    },
    d(s) {
      s && m(e), a = !1, Pe(n);
    }
  };
}
function dl(t) {
  let e, l, a, n, o, s = "Yes", p, u;
  function d(...c) {
    return (
      /*change_handler_1*/
      t[55](
        /*node*/
        t[96],
        /*field*/
        t[90],
        ...c
      )
    );
  }
  return {
    c() {
      e = k("label"), l = k("input"), n = Y(), o = k("span"), o.textContent = s, this.h();
    },
    l(c) {
      e = b(c, "LABEL", { class: !0 });
      var _ = P(e);
      l = b(_, "INPUT", { type: !0, class: !0 }), n = R(_), o = b(_, "SPAN", { "data-svelte-h": !0 }), ke(o) !== "svelte-956xxn" && (o.textContent = s), _.forEach(m), this.h();
    },
    h() {
      i(l, "type", "checkbox"), l.checked = a = W(
        /*node*/
        t[96],
        /*field*/
        t[90].key
      ) || !1, i(l, "class", "svelte-c4syt2"), i(e, "class", "property-checkbox svelte-c4syt2");
    },
    m(c, _) {
      N(c, e, _), y(e, l), y(e, n), y(e, o), p || (u = [
        T(l, "change", d),
        T(l, "click", Te(
          /*click_handler_2*/
          t[43]
        ))
      ], p = !0);
    },
    p(c, _) {
      t = c, _[0] & /*nodes, propertyFields*/
      262160 && a !== (a = W(
        /*node*/
        t[96],
        /*field*/
        t[90].key
      ) || !1) && (l.checked = a);
    },
    d(c) {
      c && m(e), p = !1, Pe(u);
    }
  };
}
function _l(t) {
  let e, l, a, n, o, s, p;
  function u(...d) {
    return (
      /*input_handler*/
      t[54](
        /*node*/
        t[96],
        /*field*/
        t[90],
        ...d
      )
    );
  }
  return {
    c() {
      e = k("input"), this.h();
    },
    l(d) {
      e = b(d, "INPUT", {
        class: !0,
        type: !0,
        min: !0,
        max: !0,
        step: !0
      }), this.h();
    },
    h() {
      i(e, "class", "property-input svelte-c4syt2"), i(e, "type", "number"), i(e, "min", l = /*field*/
      t[90].min), i(e, "max", a = /*field*/
      t[90].max), i(e, "step", n = /*field*/
      t[90].step), e.value = o = W(
        /*node*/
        t[96],
        /*field*/
        t[90].key
      ) || 0;
    },
    m(d, c) {
      N(d, e, c), s || (p = [
        T(e, "input", u),
        T(e, "click", Te(
          /*click_handler_1*/
          t[42]
        ))
      ], s = !0);
    },
    p(d, c) {
      t = d, c[0] & /*nodes, propertyFields*/
      262160 && l !== (l = /*field*/
      t[90].min) && i(e, "min", l), c[0] & /*nodes, propertyFields*/
      262160 && a !== (a = /*field*/
      t[90].max) && i(e, "max", a), c[0] & /*nodes, propertyFields*/
      262160 && n !== (n = /*field*/
      t[90].step) && i(e, "step", n), c[0] & /*nodes, propertyFields*/
      262160 && o !== (o = W(
        /*node*/
        t[96],
        /*field*/
        t[90].key
      ) || 0) && e.value !== o && (e.value = o);
    },
    d(d) {
      d && m(e), s = !1, Pe(p);
    }
  };
}
function ml(t) {
  let e, l, a, n, o = le(
    /*field*/
    t[90].options
  ), s = [];
  for (let u = 0; u < o.length; u += 1)
    s[u] = Ut(St(t, o, u));
  function p(...u) {
    return (
      /*change_handler*/
      t[53](
        /*node*/
        t[96],
        /*field*/
        t[90],
        ...u
      )
    );
  }
  return {
    c() {
      e = k("select");
      for (let u = 0; u < s.length; u += 1)
        s[u].c();
      this.h();
    },
    l(u) {
      e = b(u, "SELECT", { class: !0 });
      var d = P(e);
      for (let c = 0; c < s.length; c += 1)
        s[c].l(d);
      d.forEach(m), this.h();
    },
    h() {
      i(e, "class", "property-select svelte-c4syt2");
    },
    m(u, d) {
      N(u, e, d);
      for (let c = 0; c < s.length; c += 1)
        s[c] && s[c].m(e, null);
      gt(e, W(
        /*node*/
        t[96],
        /*field*/
        t[90].key
      ) || ""), a || (n = [
        T(e, "change", p),
        T(e, "click", Te(
          /*click_handler*/
          t[41]
        ))
      ], a = !0);
    },
    p(u, d) {
      if (t = u, d[0] & /*propertyFields, nodes*/
      262160) {
        o = le(
          /*field*/
          t[90].options
        );
        let c;
        for (c = 0; c < o.length; c += 1) {
          const _ = St(t, o, c);
          s[c] ? s[c].p(_, d) : (s[c] = Ut(_), s[c].c(), s[c].m(e, null));
        }
        for (; c < s.length; c += 1)
          s[c].d(1);
        s.length = o.length;
      }
      d[0] & /*nodes, propertyFields*/
      262160 && l !== (l = W(
        /*node*/
        t[96],
        /*field*/
        t[90].key
      ) || "") && gt(e, W(
        /*node*/
        t[96],
        /*field*/
        t[90].key
      ) || "");
    },
    d(u) {
      u && m(e), Ke(s, u), a = !1, Pe(n);
    }
  };
}
function Ut(t) {
  let e, l = (
    /*option*/
    t[93] + ""
  ), a, n;
  return {
    c() {
      e = k("option"), a = G(l), this.h();
    },
    l(o) {
      e = b(o, "OPTION", {});
      var s = P(e);
      a = U(s, l), s.forEach(m), this.h();
    },
    h() {
      e.__value = n = /*option*/
      t[93], $e(e, e.__value);
    },
    m(o, s) {
      N(o, e, s), y(e, a);
    },
    p(o, s) {
      s[0] & /*nodes*/
      16 && l !== (l = /*option*/
      o[93] + "") && ce(a, l), s[0] & /*nodes, propertyFields*/
      262160 && n !== (n = /*option*/
      o[93]) && (e.__value = n, $e(e, e.__value));
    },
    d(o) {
      o && m(e);
    }
  };
}
function Xt(t) {
  let e, l, a = (
    /*field*/
    t[90].label + ""
  ), n, o, s, p;
  function u(_, v) {
    return (
      /*field*/
      _[90].type === "select" ? ml : (
        /*field*/
        _[90].type === "number" ? _l : (
          /*field*/
          _[90].type === "checkbox" ? dl : (
            /*field*/
            _[90].type === "textarea" ? cl : ul
          )
        )
      )
    );
  }
  let d = u(t), c = d(t);
  return {
    c() {
      e = k("div"), l = k("label"), n = G(a), o = G(":"), s = Y(), c.c(), p = Y(), this.h();
    },
    l(_) {
      e = b(_, "DIV", { class: !0 });
      var v = P(e);
      l = b(v, "LABEL", { class: !0 });
      var g = P(l);
      n = U(g, a), o = U(g, ":"), g.forEach(m), s = R(v), c.l(v), p = R(v), v.forEach(m), this.h();
    },
    h() {
      i(l, "class", "property-label svelte-c4syt2"), i(e, "class", "node-property svelte-c4syt2");
    },
    m(_, v) {
      N(_, e, v), y(e, l), y(l, n), y(l, o), y(e, s), c.m(e, null), y(e, p);
    },
    p(_, v) {
      v[0] & /*nodes*/
      16 && a !== (a = /*field*/
      _[90].label + "") && ce(n, a), d === (d = u(_)) && c ? c.p(_, v) : (c.d(1), c = d(_), c && (c.c(), c.m(e, p)));
    },
    d(_) {
      _ && m(e), c.d();
    }
  };
}
function yl(t) {
  let e, l, a, n, o;
  function s(...u) {
    return (
      /*mouseup_handler_2*/
      t[62](
        /*node*/
        t[96],
        ...u
      )
    );
  }
  function p(...u) {
    return (
      /*mousedown_handler_2*/
      t[63](
        /*node*/
        t[96],
        ...u
      )
    );
  }
  return {
    c() {
      e = k("div"), l = Y(), a = k("div"), this.h();
    },
    l(u) {
      e = b(u, "DIV", { class: !0, style: !0, title: !0 }), P(e).forEach(m), l = R(u), a = b(u, "DIV", { class: !0, style: !0, title: !0 }), P(a).forEach(m), this.h();
    },
    h() {
      i(e, "class", "connection-point input svelte-c4syt2"), X(e, "top", "50%"), X(e, "left", "-6px"), X(e, "transform", "translateY(-50%)"), i(e, "title", "Input"), i(a, "class", "connection-point output svelte-c4syt2"), X(a, "top", "50%"), X(a, "right", "-6px"), X(a, "transform", "translateY(-50%)"), i(a, "title", "Output");
    },
    m(u, d) {
      N(u, e, d), N(u, l, d), N(u, a, d), n || (o = [
        T(e, "mouseup", s),
        T(a, "mousedown", p)
      ], n = !0);
    },
    p(u, d) {
      t = u;
    },
    d(u) {
      u && (m(e), m(l), m(a)), n = !1, Pe(o);
    }
  };
}
function Gt(t) {
  let e, l, a, n = le(
    /*templateHandles*/
    t[100]
  ), o = [];
  for (let u = 0; u < n.length; u += 1)
    o[u] = Wt(Ct(t, n, u));
  let s = !/*hasInputHandles*/
  t[101] && Qt(t), p = !/*hasOutputHandles*/
  t[102] && zt(t);
  return {
    c() {
      for (let u = 0; u < o.length; u += 1)
        o[u].c();
      e = Y(), s && s.c(), l = Y(), p && p.c(), a = de();
    },
    l(u) {
      for (let d = 0; d < o.length; d += 1)
        o[d].l(u);
      e = R(u), s && s.l(u), l = R(u), p && p.l(u), a = de();
    },
    m(u, d) {
      for (let c = 0; c < o.length; c += 1)
        o[c] && o[c].m(u, d);
      N(u, e, d), s && s.m(u, d), N(u, l, d), p && p.m(u, d), N(u, a, d);
    },
    p(u, d) {
      if (d[0] & /*nodes, endConnection, startConnection*/
      1610612752) {
        n = le(
          /*templateHandles*/
          u[100]
        );
        let c;
        for (c = 0; c < n.length; c += 1) {
          const _ = Ct(u, n, c);
          o[c] ? o[c].p(_, d) : (o[c] = Wt(_), o[c].c(), o[c].m(e.parentNode, e));
        }
        for (; c < o.length; c += 1)
          o[c].d(1);
        o.length = n.length;
      }
      /*hasInputHandles*/
      u[101] ? s && (s.d(1), s = null) : s ? s.p(u, d) : (s = Qt(u), s.c(), s.m(l.parentNode, l)), /*hasOutputHandles*/
      u[102] ? p && (p.d(1), p = null) : p ? p.p(u, d) : (p = zt(u), p.c(), p.m(a.parentNode, a));
    },
    d(u) {
      u && (m(e), m(l), m(a)), Ke(o, u), s && s.d(u), p && p.d(u);
    }
  };
}
function qt(t) {
  let e, l, a, n, o, s;
  function p(...d) {
    return (
      /*mouseup_handler*/
      t[58](
        /*handle*/
        t[104],
        /*node*/
        t[96],
        ...d
      )
    );
  }
  function u(...d) {
    return (
      /*mousedown_handler*/
      t[59](
        /*handle*/
        t[104],
        /*node*/
        t[96],
        ...d
      )
    );
  }
  return {
    c() {
      e = k("div"), this.h();
    },
    l(d) {
      e = b(d, "DIV", { class: !0, style: !0, title: !0 }), P(e).forEach(m), this.h();
    },
    h() {
      i(e, "class", l = "connection-point " + /*handle*/
      (t[104].type === "string" || /*handle*/
      t[104].type === "list" || /*handle*/
      t[104].type === "file" ? "output" : "input") + " svelte-c4syt2"), i(e, "style", a = "top: " + /*index*/
      (t[106] * 25 + 40) + "px; " + /*handle*/
      (t[104].type === "string" || /*handle*/
      t[104].type === "list" || /*handle*/
      t[104].type === "file" ? "right: -6px;" : "left: -6px;")), i(e, "title", n = `${/*handle*/
      t[104].display_name || /*handleId*/
      t[103]} (${/*handle*/
      t[104].type})`);
    },
    m(d, c) {
      N(d, e, c), o || (s = [
        T(e, "mouseup", p),
        T(e, "mousedown", u)
      ], o = !0);
    },
    p(d, c) {
      t = d, c[0] & /*nodes, propertyFields*/
      262160 && l !== (l = "connection-point " + /*handle*/
      (t[104].type === "string" || /*handle*/
      t[104].type === "list" || /*handle*/
      t[104].type === "file" ? "output" : "input") + " svelte-c4syt2") && i(e, "class", l), c[0] & /*nodes, propertyFields*/
      262160 && a !== (a = "top: " + /*index*/
      (t[106] * 25 + 40) + "px; " + /*handle*/
      (t[104].type === "string" || /*handle*/
      t[104].type === "list" || /*handle*/
      t[104].type === "file" ? "right: -6px;" : "left: -6px;")) && i(e, "style", a), c[0] & /*nodes, propertyFields*/
      262160 && n !== (n = `${/*handle*/
      t[104].display_name || /*handleId*/
      t[103]} (${/*handle*/
      t[104].type})`) && i(e, "title", n);
    },
    d(d) {
      d && m(e), o = !1, Pe(s);
    }
  };
}
function Wt(t) {
  let e, l = (
    /*handle*/
    (t[104].type === "string" || /*handle*/
    t[104].type === "object" || /*handle*/
    t[104].type === "list" || /*handle*/
    t[104].type === "file") && qt(t)
  );
  return {
    c() {
      l && l.c(), e = de();
    },
    l(a) {
      l && l.l(a), e = de();
    },
    m(a, n) {
      l && l.m(a, n), N(a, e, n);
    },
    p(a, n) {
      /*handle*/
      a[104].type === "string" || /*handle*/
      a[104].type === "object" || /*handle*/
      a[104].type === "list" || /*handle*/
      a[104].type === "file" ? l ? l.p(a, n) : (l = qt(a), l.c(), l.m(e.parentNode, e)) : l && (l.d(1), l = null);
    },
    d(a) {
      a && m(e), l && l.d(a);
    }
  };
}
function Qt(t) {
  let e, l, a;
  function n(...o) {
    return (
      /*mouseup_handler_1*/
      t[60](
        /*node*/
        t[96],
        ...o
      )
    );
  }
  return {
    c() {
      e = k("div"), this.h();
    },
    l(o) {
      e = b(o, "DIV", { class: !0, style: !0, title: !0 }), P(e).forEach(m), this.h();
    },
    h() {
      i(e, "class", "connection-point input svelte-c4syt2"), X(e, "top", "50%"), X(e, "left", "-6px"), X(e, "transform", "translateY(-50%)"), i(e, "title", "Input");
    },
    m(o, s) {
      N(o, e, s), l || (a = T(e, "mouseup", n), l = !0);
    },
    p(o, s) {
      t = o;
    },
    d(o) {
      o && m(e), l = !1, a();
    }
  };
}
function zt(t) {
  let e, l, a;
  function n(...o) {
    return (
      /*mousedown_handler_1*/
      t[61](
        /*node*/
        t[96],
        ...o
      )
    );
  }
  return {
    c() {
      e = k("div"), this.h();
    },
    l(o) {
      e = b(o, "DIV", { class: !0, style: !0, title: !0 }), P(e).forEach(m), this.h();
    },
    h() {
      i(e, "class", "connection-point output svelte-c4syt2"), X(e, "top", "50%"), X(e, "right", "-6px"), X(e, "transform", "translateY(-50%)"), i(e, "title", "Output");
    },
    m(o, s) {
      N(o, e, s), l || (a = T(e, "mousedown", n), l = !0);
    },
    p(o, s) {
      t = o;
    },
    d(o) {
      o && m(e), l = !1, a();
    }
  };
}
function Jt(t, e) {
  let l, a, n, o = (
    /*config*/
    e[97].icon + ""
  ), s, p, u, d = (
    /*node*/
    (e[96].data.display_name || /*node*/
    e[96].data.label) + ""
  ), c, _, v, g = "✕", h, I, E, D, A, C;
  function oe() {
    return (
      /*click_handler_7*/
      e[52](
        /*node*/
        e[96]
      )
    );
  }
  function Q(L, K) {
    return (
      /*propertyFields*/
      L[18][
        /*node*/
        L[96].type
      ] ? pl : rl
    );
  }
  let Z = Q(e), S = Z(e);
  function fe(L, K) {
    return (
      /*node*/
      L[96].data.template ? Gt : yl
    );
  }
  function ve(L, K) {
    return K === Gt ? il(L) : L;
  }
  let ae = fe(e), O = ae(ve(e, ae));
  function j(...L) {
    return (
      /*mousedown_handler_3*/
      e[64](
        /*node*/
        e[96],
        ...L
      )
    );
  }
  function Ee(...L) {
    return (
      /*click_handler_8*/
      e[65](
        /*node*/
        e[96],
        ...L
      )
    );
  }
  return {
    key: t,
    first: null,
    c() {
      l = k("div"), a = k("div"), n = k("span"), s = G(o), p = Y(), u = k("span"), c = G(d), _ = Y(), v = k("button"), v.textContent = g, h = Y(), I = k("div"), S.c(), E = Y(), O.c(), D = Y(), this.h();
    },
    l(L) {
      l = b(L, "DIV", { class: !0, style: !0 });
      var K = P(l);
      a = b(K, "DIV", { class: !0, style: !0 });
      var V = P(a);
      n = b(V, "SPAN", { class: !0 });
      var B = P(n);
      s = U(B, o), B.forEach(m), p = R(V), u = b(V, "SPAN", { class: !0 });
      var _e = P(u);
      c = U(_e, d), _e.forEach(m), _ = R(V), v = b(V, "BUTTON", {
        class: !0,
        title: !0,
        "data-svelte-h": !0
      }), ke(v) !== "svelte-18enu0f" && (v.textContent = g), V.forEach(m), h = R(K), I = b(K, "DIV", { class: !0 });
      var Me = P(I);
      S.l(Me), Me.forEach(m), E = R(K), O.l(K), D = R(K), K.forEach(m), this.h();
    },
    h() {
      var L;
      i(n, "class", "node-icon svelte-c4syt2"), i(u, "class", "node-title svelte-c4syt2"), i(v, "class", "node-delete svelte-c4syt2"), i(v, "title", "Delete node"), i(a, "class", "node-header svelte-c4syt2"), X(
        a,
        "background",
        /*config*/
        e[97].color
      ), i(I, "class", "node-content svelte-c4syt2"), i(l, "class", "node svelte-c4syt2"), X(
        l,
        "left",
        /*node*/
        e[96].position.x + "px"
      ), X(
        l,
        "top",
        /*node*/
        e[96].position.y + "px"
      ), X(
        l,
        "border-color",
        /*config*/
        e[97].color
      ), Se(
        l,
        "selected",
        /*selectedNode*/
        ((L = e[11]) == null ? void 0 : L.id) === /*node*/
        e[96].id
      ), this.first = l;
    },
    m(L, K) {
      N(L, l, K), y(l, a), y(a, n), y(n, s), y(a, p), y(a, u), y(u, c), y(a, _), y(a, v), y(l, h), y(l, I), S.m(I, null), y(l, E), O.m(l, null), y(l, D), A || (C = [
        T(v, "click", Te(oe)),
        T(l, "mousedown", j),
        T(l, "click", Ee)
      ], A = !0);
    },
    p(L, K) {
      var V;
      e = L, K[0] & /*nodes*/
      16 && o !== (o = /*config*/
      e[97].icon + "") && ce(s, o), K[0] & /*nodes*/
      16 && d !== (d = /*node*/
      (e[96].data.display_name || /*node*/
      e[96].data.label) + "") && ce(c, d), K[0] & /*nodes*/
      16 && X(
        a,
        "background",
        /*config*/
        e[97].color
      ), Z === (Z = Q(e)) && S ? S.p(e, K) : (S.d(1), S = Z(e), S && (S.c(), S.m(I, null))), ae === (ae = fe(e)) && O ? O.p(ve(e, ae), K) : (O.d(1), O = ae(ve(e, ae)), O && (O.c(), O.m(l, D))), K[0] & /*nodes*/
      16 && X(
        l,
        "left",
        /*node*/
        e[96].position.x + "px"
      ), K[0] & /*nodes*/
      16 && X(
        l,
        "top",
        /*node*/
        e[96].position.y + "px"
      ), K[0] & /*nodes*/
      16 && X(
        l,
        "border-color",
        /*config*/
        e[97].color
      ), K[0] & /*selectedNode, nodes*/
      2064 && Se(
        l,
        "selected",
        /*selectedNode*/
        ((V = e[11]) == null ? void 0 : V.id) === /*node*/
        e[96].id
      );
    },
    d(L) {
      L && m(l), S.d(), O.d(), A = !1, Pe(C);
    }
  };
}
function Zt(t) {
  let e, l = "Properties";
  return {
    c() {
      e = k("h3"), e.textContent = l, this.h();
    },
    l(a) {
      e = b(a, "H3", { class: !0, "data-svelte-h": !0 }), ke(e) !== "svelte-mbvbrx" && (e.textContent = l), this.h();
    },
    h() {
      i(e, "class", "svelte-c4syt2");
    },
    m(a, n) {
      N(a, e, n);
    },
    d(a) {
      a && m(e);
    }
  };
}
function xt(t) {
  let e;
  function l(o, s) {
    return (
      /*selectedNode*/
      o[11] && /*propertyFields*/
      o[18][
        /*selectedNode*/
        o[11].type
      ] ? fl : hl
    );
  }
  let a = l(t), n = a(t);
  return {
    c() {
      e = k("div"), n.c(), this.h();
    },
    l(o) {
      e = b(o, "DIV", { class: !0 });
      var s = P(e);
      n.l(s), s.forEach(m), this.h();
    },
    h() {
      i(e, "class", "property-content svelte-c4syt2");
    },
    m(o, s) {
      N(o, e, s), n.m(e, null);
    },
    p(o, s) {
      a === (a = l(o)) && n ? n.p(o, s) : (n.d(1), n = a(o), n && (n.c(), n.m(e, null)));
    },
    d(o) {
      o && m(e), n.d();
    }
  };
}
function hl(t) {
  let e, l = '<div class="empty-icon svelte-c4syt2">🎯</div> <p class="svelte-c4syt2">Select a node to edit properties</p> <small class="svelte-c4syt2">Click on any node to configure its detailed settings</small>';
  return {
    c() {
      e = k("div"), e.innerHTML = l, this.h();
    },
    l(a) {
      e = b(a, "DIV", { class: !0, "data-svelte-h": !0 }), ke(e) !== "svelte-aa72n1" && (e.innerHTML = l), this.h();
    },
    h() {
      i(e, "class", "property-empty svelte-c4syt2");
    },
    m(a, n) {
      N(a, e, n);
    },
    p: vt,
    d(a) {
      a && m(e);
    }
  };
}
function fl(t) {
  let e, l, a = (
    /*selectedNode*/
    (t[11].data.display_name || /*selectedNode*/
    t[11].data.label) + ""
  ), n, o, s, p, u = (
    /*selectedNode*/
    t[11].type.toUpperCase() + ""
  ), d, c, _, v = le(
    /*propertyFields*/
    t[18][
      /*selectedNode*/
      t[11].type
    ]
  ), g = [];
  for (let h = 0; h < v.length; h += 1)
    g[h] = tl(Dt(t, v, h));
  return {
    c() {
      e = k("div"), l = k("h4"), n = G(a), o = Y(), s = k("p"), p = G("TYPE: "), d = G(u), c = Y(), _ = k("div");
      for (let h = 0; h < g.length; h += 1)
        g[h].c();
      this.h();
    },
    l(h) {
      e = b(h, "DIV", { class: !0 });
      var I = P(e);
      l = b(I, "H4", { class: !0 });
      var E = P(l);
      n = U(E, a), E.forEach(m), o = R(I), s = b(I, "P", { class: !0 });
      var D = P(s);
      p = U(D, "TYPE: "), d = U(D, u), D.forEach(m), I.forEach(m), c = R(h), _ = b(h, "DIV", { class: !0 });
      var A = P(_);
      for (let C = 0; C < g.length; C += 1)
        g[C].l(A);
      A.forEach(m), this.h();
    },
    h() {
      i(l, "class", "svelte-c4syt2"), i(s, "class", "property-node-type svelte-c4syt2"), i(e, "class", "property-node-info svelte-c4syt2"), i(_, "class", "property-fields");
    },
    m(h, I) {
      N(h, e, I), y(e, l), y(l, n), y(e, o), y(e, s), y(s, p), y(s, d), N(h, c, I), N(h, _, I);
      for (let E = 0; E < g.length; E += 1)
        g[E] && g[E].m(_, null);
    },
    p(h, I) {
      if (I[0] & /*selectedNode*/
      2048 && a !== (a = /*selectedNode*/
      (h[11].data.display_name || /*selectedNode*/
      h[11].data.label) + "") && ce(n, a), I[0] & /*selectedNode*/
      2048 && u !== (u = /*selectedNode*/
      h[11].type.toUpperCase() + "") && ce(d, u), I[0] & /*propertyFields, selectedNode*/
      264192 | I[1] & /*updateNodeProperty*/
      4) {
        v = le(
          /*propertyFields*/
          h[18][
            /*selectedNode*/
            h[11].type
          ]
        );
        let E;
        for (E = 0; E < v.length; E += 1) {
          const D = Dt(h, v, E);
          g[E] ? g[E].p(D, I) : (g[E] = tl(D), g[E].c(), g[E].m(_, null));
        }
        for (; E < g.length; E += 1)
          g[E].d(1);
        g.length = v.length;
      }
    },
    d(h) {
      h && (m(e), m(c), m(_)), Ke(g, h);
    }
  };
}
function $t(t) {
  let e, l = (
    /*field*/
    t[90].help + ""
  ), a;
  return {
    c() {
      e = k("small"), a = G(l), this.h();
    },
    l(n) {
      e = b(n, "SMALL", { class: !0 });
      var o = P(e);
      a = U(o, l), o.forEach(m), this.h();
    },
    h() {
      i(e, "class", "field-help svelte-c4syt2");
    },
    m(n, o) {
      N(n, e, o), y(e, a);
    },
    p(n, o) {
      o[0] & /*selectedNode*/
      2048 && l !== (l = /*field*/
      n[90].help + "") && ce(a, l);
    },
    d(n) {
      n && m(e);
    }
  };
}
function vl(t) {
  let e, l, a, n, o;
  function s(...p) {
    return (
      /*input_handler_5*/
      t[73](
        /*field*/
        t[90],
        ...p
      )
    );
  }
  return {
    c() {
      e = k("textarea"), this.h();
    },
    l(p) {
      e = b(p, "TEXTAREA", { id: !0, rows: !0, class: !0 }), P(e).forEach(m), this.h();
    },
    h() {
      i(e, "id", l = /*field*/
      t[90].key), e.value = a = W(
        /*selectedNode*/
        t[11],
        /*field*/
        t[90].key
      ) || "", i(e, "rows", "4"), i(e, "class", "svelte-c4syt2");
    },
    m(p, u) {
      N(p, e, u), n || (o = T(e, "input", s), n = !0);
    },
    p(p, u) {
      t = p, u[0] & /*selectedNode, propertyFields*/
      264192 && l !== (l = /*field*/
      t[90].key) && i(e, "id", l), u[0] & /*selectedNode, propertyFields*/
      264192 && a !== (a = W(
        /*selectedNode*/
        t[11],
        /*field*/
        t[90].key
      ) || "") && (e.value = a);
    },
    d(p) {
      p && m(e), n = !1, o();
    }
  };
}
function gl(t) {
  let e, l, a, n, o, s = le(
    /*field*/
    t[90].options
  ), p = [];
  for (let d = 0; d < s.length; d += 1)
    p[d] = el(Mt(t, s, d));
  function u(...d) {
    return (
      /*change_handler_3*/
      t[72](
        /*field*/
        t[90],
        ...d
      )
    );
  }
  return {
    c() {
      e = k("select");
      for (let d = 0; d < p.length; d += 1)
        p[d].c();
      this.h();
    },
    l(d) {
      e = b(d, "SELECT", { id: !0, class: !0 });
      var c = P(e);
      for (let _ = 0; _ < p.length; _ += 1)
        p[_].l(c);
      c.forEach(m), this.h();
    },
    h() {
      i(e, "id", l = /*field*/
      t[90].key), i(e, "class", "svelte-c4syt2");
    },
    m(d, c) {
      N(d, e, c);
      for (let _ = 0; _ < p.length; _ += 1)
        p[_] && p[_].m(e, null);
      gt(e, W(
        /*selectedNode*/
        t[11],
        /*field*/
        t[90].key
      ) || ""), n || (o = T(e, "change", u), n = !0);
    },
    p(d, c) {
      if (t = d, c[0] & /*propertyFields, selectedNode*/
      264192) {
        s = le(
          /*field*/
          t[90].options
        );
        let _;
        for (_ = 0; _ < s.length; _ += 1) {
          const v = Mt(t, s, _);
          p[_] ? p[_].p(v, c) : (p[_] = el(v), p[_].c(), p[_].m(e, null));
        }
        for (; _ < p.length; _ += 1)
          p[_].d(1);
        p.length = s.length;
      }
      c[0] & /*selectedNode, propertyFields*/
      264192 && l !== (l = /*field*/
      t[90].key) && i(e, "id", l), c[0] & /*selectedNode, propertyFields*/
      264192 && a !== (a = W(
        /*selectedNode*/
        t[11],
        /*field*/
        t[90].key
      ) || "") && gt(e, W(
        /*selectedNode*/
        t[11],
        /*field*/
        t[90].key
      ) || "");
    },
    d(d) {
      d && m(e), Ke(p, d), n = !1, o();
    }
  };
}
function bl(t) {
  let e, l, a, n, o, s, p = "Enable", u, d;
  function c(..._) {
    return (
      /*change_handler_2*/
      t[71](
        /*field*/
        t[90],
        ..._
      )
    );
  }
  return {
    c() {
      e = k("label"), l = k("input"), o = Y(), s = k("span"), s.textContent = p, this.h();
    },
    l(_) {
      e = b(_, "LABEL", { class: !0 });
      var v = P(e);
      l = b(v, "INPUT", { type: !0, id: !0, class: !0 }), o = R(v), s = b(v, "SPAN", { class: !0, "data-svelte-h": !0 }), ke(s) !== "svelte-k3h2i9" && (s.textContent = p), v.forEach(m), this.h();
    },
    h() {
      i(l, "type", "checkbox"), i(l, "id", a = /*field*/
      t[90].key), l.checked = n = W(
        /*selectedNode*/
        t[11],
        /*field*/
        t[90].key
      ) || !1, i(l, "class", "svelte-c4syt2"), i(s, "class", "checkbox-text"), i(e, "class", "checkbox-label svelte-c4syt2");
    },
    m(_, v) {
      N(_, e, v), y(e, l), y(e, o), y(e, s), u || (d = T(l, "change", c), u = !0);
    },
    p(_, v) {
      t = _, v[0] & /*selectedNode, propertyFields*/
      264192 && a !== (a = /*field*/
      t[90].key) && i(l, "id", a), v[0] & /*selectedNode, propertyFields*/
      264192 && n !== (n = W(
        /*selectedNode*/
        t[11],
        /*field*/
        t[90].key
      ) || !1) && (l.checked = n);
    },
    d(_) {
      _ && m(e), u = !1, d();
    }
  };
}
function kl(t) {
  let e, l, a, n, o, s, p, u;
  function d(...c) {
    return (
      /*input_handler_4*/
      t[70](
        /*field*/
        t[90],
        ...c
      )
    );
  }
  return {
    c() {
      e = k("input"), this.h();
    },
    l(c) {
      e = b(c, "INPUT", {
        type: !0,
        id: !0,
        min: !0,
        max: !0,
        step: !0,
        class: !0
      }), this.h();
    },
    h() {
      i(e, "type", "number"), i(e, "id", l = /*field*/
      t[90].key), e.value = a = W(
        /*selectedNode*/
        t[11],
        /*field*/
        t[90].key
      ) || 0, i(e, "min", n = /*field*/
      t[90].min), i(e, "max", o = /*field*/
      t[90].max), i(e, "step", s = /*field*/
      t[90].step), i(e, "class", "svelte-c4syt2");
    },
    m(c, _) {
      N(c, e, _), p || (u = T(e, "input", d), p = !0);
    },
    p(c, _) {
      t = c, _[0] & /*selectedNode, propertyFields*/
      264192 && l !== (l = /*field*/
      t[90].key) && i(e, "id", l), _[0] & /*selectedNode, propertyFields*/
      264192 && a !== (a = W(
        /*selectedNode*/
        t[11],
        /*field*/
        t[90].key
      ) || 0) && e.value !== a && (e.value = a), _[0] & /*selectedNode, propertyFields*/
      264192 && n !== (n = /*field*/
      t[90].min) && i(e, "min", n), _[0] & /*selectedNode, propertyFields*/
      264192 && o !== (o = /*field*/
      t[90].max) && i(e, "max", o), _[0] & /*selectedNode, propertyFields*/
      264192 && s !== (s = /*field*/
      t[90].step) && i(e, "step", s);
    },
    d(c) {
      c && m(e), p = !1, u();
    }
  };
}
function wl(t) {
  let e, l, a, n, o;
  function s(...p) {
    return (
      /*input_handler_3*/
      t[69](
        /*field*/
        t[90],
        ...p
      )
    );
  }
  return {
    c() {
      e = k("input"), this.h();
    },
    l(p) {
      e = b(p, "INPUT", { type: !0, id: !0, class: !0 }), this.h();
    },
    h() {
      i(e, "type", "text"), i(e, "id", l = /*field*/
      t[90].key), e.value = a = W(
        /*selectedNode*/
        t[11],
        /*field*/
        t[90].key
      ) || "", i(e, "class", "svelte-c4syt2");
    },
    m(p, u) {
      N(p, e, u), n || (o = T(e, "input", s), n = !0);
    },
    p(p, u) {
      t = p, u[0] & /*selectedNode, propertyFields*/
      264192 && l !== (l = /*field*/
      t[90].key) && i(e, "id", l), u[0] & /*selectedNode, propertyFields*/
      264192 && a !== (a = W(
        /*selectedNode*/
        t[11],
        /*field*/
        t[90].key
      ) || "") && e.value !== a && (e.value = a);
    },
    d(p) {
      p && m(e), n = !1, o();
    }
  };
}
function el(t) {
  let e, l = (
    /*option*/
    t[93] + ""
  ), a, n;
  return {
    c() {
      e = k("option"), a = G(l), this.h();
    },
    l(o) {
      e = b(o, "OPTION", {});
      var s = P(e);
      a = U(s, l), s.forEach(m), this.h();
    },
    h() {
      e.__value = n = /*option*/
      t[93], $e(e, e.__value);
    },
    m(o, s) {
      N(o, e, s), y(e, a);
    },
    p(o, s) {
      s[0] & /*selectedNode*/
      2048 && l !== (l = /*option*/
      o[93] + "") && ce(a, l), s[0] & /*selectedNode, propertyFields*/
      264192 && n !== (n = /*option*/
      o[93]) && (e.__value = n, $e(e, e.__value));
    },
    d(o) {
      o && m(e);
    }
  };
}
function tl(t) {
  let e, l, a = (
    /*field*/
    t[90].label + ""
  ), n, o, s, p, u, d = (
    /*field*/
    t[90].help && $t(t)
  );
  function c(g, h) {
    if (
      /*field*/
      g[90].type === "text"
    ) return wl;
    if (
      /*field*/
      g[90].type === "number"
    ) return kl;
    if (
      /*field*/
      g[90].type === "checkbox"
    ) return bl;
    if (
      /*field*/
      g[90].type === "select"
    ) return gl;
    if (
      /*field*/
      g[90].type === "textarea"
    ) return vl;
  }
  let _ = c(t), v = _ && _(t);
  return {
    c() {
      e = k("div"), l = k("label"), n = G(a), s = Y(), d && d.c(), p = Y(), v && v.c(), u = Y(), this.h();
    },
    l(g) {
      e = b(g, "DIV", { class: !0 });
      var h = P(e);
      l = b(h, "LABEL", { for: !0, class: !0 });
      var I = P(l);
      n = U(I, a), I.forEach(m), s = R(h), d && d.l(h), p = R(h), v && v.l(h), u = R(h), h.forEach(m), this.h();
    },
    h() {
      i(l, "for", o = /*field*/
      t[90].key), i(l, "class", "svelte-c4syt2"), i(e, "class", "property-field svelte-c4syt2");
    },
    m(g, h) {
      N(g, e, h), y(e, l), y(l, n), y(e, s), d && d.m(e, null), y(e, p), v && v.m(e, null), y(e, u);
    },
    p(g, h) {
      h[0] & /*selectedNode*/
      2048 && a !== (a = /*field*/
      g[90].label + "") && ce(n, a), h[0] & /*selectedNode, propertyFields*/
      264192 && o !== (o = /*field*/
      g[90].key) && i(l, "for", o), /*field*/
      g[90].help ? d ? d.p(g, h) : (d = $t(g), d.c(), d.m(e, p)) : d && (d.d(1), d = null), _ === (_ = c(g)) && v ? v.p(g, h) : (v && v.d(1), v = _ && _(g), v && (v.c(), v.m(e, u)));
    },
    d(g) {
      g && m(e), d && d.d(), v && v.d();
    }
  };
}
function Il(t) {
  let e, l, a, n, o, s, p = (
    /*sidebarCollapsed*/
    t[12] ? "→" : "←"
  ), u, d, c, _, v, g, h, I, E, D, A, C, oe = "-", Q, Z, S = Math.round(
    /*zoomLevel*/
    t[15] * 100
  ) + "", fe, ve, ae, O, j = "+", Ee, L, K = "⌂", V, B, _e, Me, Oe = (
    /*nodes*/
    t[4].length + ""
  ), je, et, De, tt, Re = (
    /*edges*/
    t[5].length + ""
  ), Be, lt, ye, pt = "🗑️ Clear", He, we, q, Ne, Ce, re, pe = [], Ue = /* @__PURE__ */ new Map(), ie, at, ue = [], ut = /* @__PURE__ */ new Map(), nt, me, ge, Xe, be, Ye = (
    /*propertyPanelCollapsed*/
    t[13] ? "←" : "→"
  ), Ge, qe, st, We, ot, ct, ne = !/*sidebarCollapsed*/
  t[12] && Yt(), x = !/*sidebarCollapsed*/
  t[12] && Lt(t), Qe = le(
    /*edges*/
    t[5]
  );
  const dt = (w) => (
    /*edge*/
    w[112].id
  );
  for (let w = 0; w < Qe.length; w += 1) {
    let M = Tt(t, Qe, w), H = dt(M);
    Ue.set(H, pe[w] = jt(H, M));
  }
  let $ = (
    /*isConnecting*/
    t[8] && /*connectionStart*/
    t[9] && Bt(bt(t))
  ), ze = le(
    /*nodes*/
    t[4]
  );
  const _t = (w) => (
    /*node*/
    w[96].id
  );
  for (let w = 0; w < ze.length; w += 1) {
    let M = Nt(t, ze, w), H = _t(M);
    ut.set(H, ue[w] = Jt(H, M));
  }
  let se = !/*propertyPanelCollapsed*/
  t[13] && Zt(), ee = !/*propertyPanelCollapsed*/
  t[13] && xt(t);
  return {
    c() {
      e = k("div"), l = k("div"), a = k("div"), n = k("div"), ne && ne.c(), o = Y(), s = k("button"), u = G(p), c = Y(), x && x.c(), _ = Y(), v = k("div"), g = k("div"), h = k("div"), I = k("input"), E = Y(), D = k("div"), A = k("div"), C = k("button"), C.textContent = oe, Q = Y(), Z = k("span"), fe = G(S), ve = G("%"), ae = Y(), O = k("button"), O.textContent = j, Ee = Y(), L = k("button"), L.textContent = K, V = Y(), B = k("div"), _e = k("span"), Me = G("Nodes: "), je = G(Oe), et = Y(), De = k("span"), tt = G("Edges: "), Be = G(Re), lt = Y(), ye = k("button"), ye.textContent = pt, He = Y(), we = k("div"), q = k("div"), Ne = k("div"), Ce = Y(), re = Ve("svg");
      for (let w = 0; w < pe.length; w += 1)
        pe[w].c();
      ie = de(), $ && $.c(), at = Y();
      for (let w = 0; w < ue.length; w += 1)
        ue[w].c();
      nt = Y(), me = k("div"), ge = k("div"), se && se.c(), Xe = Y(), be = k("button"), Ge = G(Ye), st = Y(), ee && ee.c(), this.h();
    },
    l(w) {
      e = b(w, "DIV", { class: !0, id: !0 });
      var M = P(e);
      l = b(M, "DIV", { class: !0 });
      var H = P(l);
      a = b(H, "DIV", { class: !0 });
      var Je = P(a);
      n = b(Je, "DIV", { class: !0 });
      var Ze = P(n);
      ne && ne.l(Ze), o = R(Ze), s = b(Ze, "BUTTON", { class: !0, title: !0 });
      var mt = P(s);
      u = U(mt, p), mt.forEach(m), Ze.forEach(m), c = R(Je), x && x.l(Je), Je.forEach(m), _ = R(H), v = b(H, "DIV", { class: !0 });
      var xe = P(v);
      g = b(xe, "DIV", { class: !0 });
      var Ae = P(g);
      h = b(Ae, "DIV", { class: !0 });
      var yt = P(h);
      I = b(yt, "INPUT", {
        class: !0,
        type: !0,
        placeholder: !0,
        title: !0
      }), yt.forEach(m), E = R(Ae), D = b(Ae, "DIV", { class: !0 });
      var ht = P(D);
      A = b(ht, "DIV", { class: !0 });
      var Ie = P(A);
      C = b(Ie, "BUTTON", {
        class: !0,
        title: !0,
        "data-svelte-h": !0
      }), ke(C) !== "svelte-1q3p1i9" && (C.textContent = oe), Q = R(Ie), Z = b(Ie, "SPAN", { class: !0 });
      var it = P(Z);
      fe = U(it, S), ve = U(it, "%"), it.forEach(m), ae = R(Ie), O = b(Ie, "BUTTON", {
        class: !0,
        title: !0,
        "data-svelte-h": !0
      }), ke(O) !== "svelte-1ugjjy9" && (O.textContent = j), Ee = R(Ie), L = b(Ie, "BUTTON", {
        class: !0,
        title: !0,
        "data-svelte-h": !0
      }), ke(L) !== "svelte-dw5791" && (L.textContent = K), Ie.forEach(m), ht.forEach(m), V = R(Ae), B = b(Ae, "DIV", { class: !0 });
      var r = P(B);
      _e = b(r, "SPAN", { class: !0 });
      var f = P(_e);
      Me = U(f, "Nodes: "), je = U(f, Oe), f.forEach(m), et = R(r), De = b(r, "SPAN", { class: !0 });
      var F = P(De);
      tt = U(F, "Edges: "), Be = U(F, Re), F.forEach(m), lt = R(r), ye = b(r, "BUTTON", {
        class: !0,
        title: !0,
        "data-svelte-h": !0
      }), ke(ye) !== "svelte-38q2s3" && (ye.textContent = pt), r.forEach(m), Ae.forEach(m), He = R(xe), we = b(xe, "DIV", { class: !0 });
      var z = P(we);
      q = b(z, "DIV", { class: !0, style: !0 });
      var J = P(q);
      Ne = b(J, "DIV", { class: !0 }), P(Ne).forEach(m), Ce = R(J), re = Fe(J, "svg", { class: !0 });
      var te = P(re);
      for (let Le = 0; Le < pe.length; Le += 1)
        pe[Le].l(te);
      ie = de(), $ && $.l(te), te.forEach(m), at = R(J);
      for (let Le = 0; Le < ue.length; Le += 1)
        ue[Le].l(J);
      J.forEach(m), z.forEach(m), xe.forEach(m), nt = R(H), me = b(H, "DIV", { class: !0 });
      var he = P(me);
      ge = b(he, "DIV", { class: !0 });
      var ft = P(ge);
      se && se.l(ft), Xe = R(ft), be = b(ft, "BUTTON", { class: !0, title: !0 });
      var wt = P(be);
      Ge = U(wt, Ye), wt.forEach(m), ft.forEach(m), st = R(he), ee && ee.l(he), he.forEach(m), H.forEach(m), M.forEach(m), this.h();
    },
    h() {
      i(s, "class", "toggle-btn sidebar-toggle svelte-c4syt2"), i(s, "title", d = /*sidebarCollapsed*/
      t[12] ? "Expand sidebar" : "Collapse sidebar"), i(n, "class", "sidebar-header svelte-c4syt2"), i(a, "class", "sidebar svelte-c4syt2"), Se(
        a,
        "collapsed",
        /*sidebarCollapsed*/
        t[12]
      ), i(I, "class", "workflow-name-input svelte-c4syt2"), i(I, "type", "text"), i(I, "placeholder", "Workflow Name"), i(I, "title", "Enter workflow name"), i(h, "class", "toolbar-left"), i(C, "class", "zoom-btn svelte-c4syt2"), i(C, "title", "Zoom Out"), i(Z, "class", "zoom-level svelte-c4syt2"), i(O, "class", "zoom-btn svelte-c4syt2"), i(O, "title", "Zoom In"), i(L, "class", "zoom-btn reset svelte-c4syt2"), i(L, "title", "Reset View"), i(A, "class", "zoom-controls svelte-c4syt2"), i(D, "class", "toolbar-center svelte-c4syt2"), i(_e, "class", "node-count svelte-c4syt2"), i(De, "class", "edge-count svelte-c4syt2"), i(ye, "class", "clear-btn svelte-c4syt2"), i(ye, "title", "Clear Workflow"), i(B, "class", "toolbar-right svelte-c4syt2"), i(g, "class", "toolbar svelte-c4syt2"), i(Ne, "class", "grid-background svelte-c4syt2"), i(re, "class", "edges-layer svelte-c4syt2"), i(q, "class", "canvas svelte-c4syt2"), X(q, "transform", "scale(" + /*zoomLevel*/
      t[15] + ") translate(" + /*panOffset*/
      t[16].x / /*zoomLevel*/
      t[15] + "px, " + /*panOffset*/
      t[16].y / /*zoomLevel*/
      t[15] + "px)"), i(we, "class", "canvas-container svelte-c4syt2"), i(v, "class", "canvas-area svelte-c4syt2"), i(be, "class", "toggle-btn property-toggle svelte-c4syt2"), i(be, "title", qe = /*propertyPanelCollapsed*/
      t[13] ? "Expand properties" : "Collapse properties"), i(ge, "class", "property-header svelte-c4syt2"), i(me, "class", "property-panel svelte-c4syt2"), Se(
        me,
        "collapsed",
        /*propertyPanelCollapsed*/
        t[13]
      ), i(l, "class", "top-section svelte-c4syt2"), i(e, "class", We = "workflow-builder " + /*elem_classes*/
      t[1].join(" ") + " svelte-c4syt2"), i(
        e,
        "id",
        /*elem_id*/
        t[0]
      ), Se(e, "hide", !/*visible*/
      t[2]), X(
        e,
        "min-width",
        /*min_width*/
        t[3] && /*min_width*/
        t[3] + "px"
      );
    },
    m(w, M) {
      N(w, e, M), y(e, l), y(l, a), y(a, n), ne && ne.m(n, null), y(n, o), y(n, s), y(s, u), y(a, c), x && x.m(a, null), y(l, _), y(l, v), y(v, g), y(g, h), y(h, I), $e(
        I,
        /*workflowName*/
        t[14]
      ), y(g, E), y(g, D), y(D, A), y(A, C), y(A, Q), y(A, Z), y(Z, fe), y(Z, ve), y(A, ae), y(A, O), y(A, Ee), y(A, L), y(g, V), y(g, B), y(B, _e), y(_e, Me), y(_e, je), y(B, et), y(B, De), y(De, tt), y(De, Be), y(B, lt), y(B, ye), y(v, He), y(v, we), y(we, q), y(q, Ne), y(q, Ce), y(q, re);
      for (let H = 0; H < pe.length; H += 1)
        pe[H] && pe[H].m(re, null);
      y(re, ie), $ && $.m(re, null), y(q, at);
      for (let H = 0; H < ue.length; H += 1)
        ue[H] && ue[H].m(q, null);
      t[66](q), t[68](we), y(l, nt), y(l, me), y(me, ge), se && se.m(ge, null), y(ge, Xe), y(ge, be), y(be, Ge), y(me, st), ee && ee.m(me, null), ot || (ct = [
        T(
          s,
          "click",
          /*toggleSidebar*/
          t[34]
        ),
        T(
          I,
          "input",
          /*input_input_handler*/
          t[47]
        ),
        T(
          C,
          "click",
          /*zoomOut*/
          t[21]
        ),
        T(
          O,
          "click",
          /*zoomIn*/
          t[20]
        ),
        T(
          L,
          "click",
          /*resetZoom*/
          t[22]
        ),
        T(
          ye,
          "click",
          /*clearWorkflow*/
          t[19]
        ),
        T(
          q,
          "drop",
          /*handleCanvasDropFromSidebar*/
          t[26]
        ),
        T(q, "dragover", Pl),
        T(
          q,
          "wheel",
          /*handleWheel*/
          t[23]
        ),
        T(
          q,
          "mousedown",
          /*startPanning*/
          t[24]
        ),
        T(
          q,
          "click",
          /*click_handler_9*/
          t[67]
        ),
        T(
          be,
          "click",
          /*togglePropertyPanel*/
          t[35]
        )
      ], ot = !0);
    },
    p(w, M) {
      /*sidebarCollapsed*/
      w[12] ? ne && (ne.d(1), ne = null) : ne || (ne = Yt(), ne.c(), ne.m(n, o)), M[0] & /*sidebarCollapsed*/
      4096 && p !== (p = /*sidebarCollapsed*/
      w[12] ? "→" : "←") && ce(u, p), M[0] & /*sidebarCollapsed*/
      4096 && d !== (d = /*sidebarCollapsed*/
      w[12] ? "Expand sidebar" : "Collapse sidebar") && i(s, "title", d), /*sidebarCollapsed*/
      w[12] ? x && (x.d(1), x = null) : x ? x.p(w, M) : (x = Lt(w), x.c(), x.m(a, null)), M[0] & /*sidebarCollapsed*/
      4096 && Se(
        a,
        "collapsed",
        /*sidebarCollapsed*/
        w[12]
      ), M[0] & /*workflowName*/
      16384 && I.value !== /*workflowName*/
      w[14] && $e(
        I,
        /*workflowName*/
        w[14]
      ), M[0] & /*zoomLevel*/
      32768 && S !== (S = Math.round(
        /*zoomLevel*/
        w[15] * 100
      ) + "") && ce(fe, S), M[0] & /*nodes*/
      16 && Oe !== (Oe = /*nodes*/
      w[4].length + "") && ce(je, Oe), M[0] & /*edges*/
      32 && Re !== (Re = /*edges*/
      w[5].length + "") && ce(Be, Re), M[0] & /*nodes, edges*/
      48 | M[1] & /*deleteEdge*/
      2 && (Qe = le(
        /*edges*/
        w[5]
      ), pe = Et(pe, M, dt, 1, w, Qe, Ue, re, Pt, jt, ie, Tt)), /*isConnecting*/
      w[8] && /*connectionStart*/
      w[9] ? $ ? $.p(bt(w), M) : ($ = Bt(bt(w)), $.c(), $.m(re, null)) : $ && ($.d(1), $ = null), M[0] & /*nodes, selectedNode, handleMouseDown, handleNodeClick, startConnection, endConnection, propertyFields*/
      2013530128 | M[1] & /*getComponentConfig, updateNodeProperty, deleteNode*/
      37 && (ze = le(
        /*nodes*/
        w[4]
      ), ue = Et(ue, M, _t, 1, w, ze, ut, q, Pt, Jt, null, Nt)), M[0] & /*zoomLevel, panOffset*/
      98304 && X(q, "transform", "scale(" + /*zoomLevel*/
      w[15] + ") translate(" + /*panOffset*/
      w[16].x / /*zoomLevel*/
      w[15] + "px, " + /*panOffset*/
      w[16].y / /*zoomLevel*/
      w[15] + "px)"), /*propertyPanelCollapsed*/
      w[13] ? se && (se.d(1), se = null) : se || (se = Zt(), se.c(), se.m(ge, Xe)), M[0] & /*propertyPanelCollapsed*/
      8192 && Ye !== (Ye = /*propertyPanelCollapsed*/
      w[13] ? "←" : "→") && ce(Ge, Ye), M[0] & /*propertyPanelCollapsed*/
      8192 && qe !== (qe = /*propertyPanelCollapsed*/
      w[13] ? "Expand properties" : "Collapse properties") && i(be, "title", qe), /*propertyPanelCollapsed*/
      w[13] ? ee && (ee.d(1), ee = null) : ee ? ee.p(w, M) : (ee = xt(w), ee.c(), ee.m(me, null)), M[0] & /*propertyPanelCollapsed*/
      8192 && Se(
        me,
        "collapsed",
        /*propertyPanelCollapsed*/
        w[13]
      ), M[0] & /*elem_classes*/
      2 && We !== (We = "workflow-builder " + /*elem_classes*/
      w[1].join(" ") + " svelte-c4syt2") && i(e, "class", We), M[0] & /*elem_id*/
      1 && i(
        e,
        "id",
        /*elem_id*/
        w[0]
      ), M[0] & /*elem_classes, visible*/
      6 && Se(e, "hide", !/*visible*/
      w[2]), M[0] & /*min_width*/
      8 && X(
        e,
        "min-width",
        /*min_width*/
        w[3] && /*min_width*/
        w[3] + "px"
      );
    },
    i: vt,
    o: vt,
    d(w) {
      w && m(e), ne && ne.d(), x && x.d();
      for (let M = 0; M < pe.length; M += 1)
        pe[M].d();
      $ && $.d();
      for (let M = 0; M < ue.length; M += 1)
        ue[M].d();
      t[66](null), t[68](null), se && se.d(), ee && ee.d(), ot = !1, Pe(ct);
    }
  };
}
function Pl(t) {
  t.preventDefault();
}
function W(t, e) {
  const l = e.split(".");
  let a = t.data;
  for (const n of l)
    a = a == null ? void 0 : a[n];
  return a;
}
function El(t, e) {
  const l = t.position.x + 320, a = t.position.y + 80, n = e.position.x, o = e.position.y + 80;
  return { sourceX: l, sourceY: a, targetX: n, targetY: o };
}
function Dl(t, e, l) {
  var a, n;
  let { value: o = { nodes: [], edges: [] } } = e, { elem_id: s = "" } = e, { elem_classes: p = [] } = e, { visible: u = !0 } = e;
  const d = !0, c = null;
  let { min_width: _ = void 0 } = e;
  const v = {}, g = sl();
  let h, I, E = !1, D = !1, A = null, C = { x: 0, y: 0 }, oe = !1, Q = null, Z = { x: 0, y: 0 }, S = null, fe = !1, ve = !1, ae = "My Workflow", O = 0.6, j = { x: 0, y: 0 }, Ee = !1, L = { x: 0, y: 0 };
  const K = {
    workflow_id: "simple-rag-v1",
    workflow_name: "Simple RAG Workflow",
    nodes: [
      {
        id: "Input-1",
        type: "Input",
        position: { x: 30, y: 100 },
        data: {
          label: "Input",
          display_name: "User Question",
          template: {
            data_type: {
              display_name: "Data Type",
              type: "options",
              options: ["string", "image", "video", "audio", "file"],
              value: "string"
            },
            value: {
              display_name: "Value or Path",
              type: "string",
              value: "How do I get started with Modal?"
            },
            data: {
              display_name: "Output Data",
              type: "object",
              is_handle: !0
            }
          },
          resources: { cpu: 0.1, memory: "128Mi", gpu: "none" }
        }
      },
      {
        id: "KnowledgeBase-1",
        type: "KnowledgeBase",
        position: { x: 50, y: 500 },
        data: {
          label: "Knowledge Base",
          display_name: "Create Product Docs KB",
          template: {
            kb_name: {
              display_name: "Knowledge Base Name",
              type: "string",
              value: "product-docs-v1"
            },
            source_type: {
              display_name: "Source Type",
              type: "options",
              options: ["Directory", "URL"],
              value: "URL"
            },
            path_or_url: {
              display_name: "Path or URL",
              type: "string",
              value: "https://modal.com/docs/guide"
            },
            knowledge_base: {
              display_name: "Knowledge Base Out",
              type: "object",
              is_handle: !0
            }
          },
          resources: { cpu: 0.2, memory: "256Mi", gpu: "none" }
        }
      },
      {
        id: "RAGQuery-1",
        type: "RAGQuery",
        position: { x: 400, y: 300 },
        data: {
          label: "RAG Query",
          display_name: "Retrieve & Augment Prompt",
          template: {
            query: {
              display_name: "Original Query",
              type: "string",
              is_handle: !0
            },
            knowledge_base: {
              display_name: "Knowledge Base",
              type: "object",
              is_handle: !0
            },
            rag_prompt: {
              display_name: "Augmented Prompt Out",
              type: "string",
              is_handle: !0
            }
          },
          resources: { cpu: 0.3, memory: "512Mi", gpu: "none" }
        }
      },
      {
        id: "ChatModel-1",
        type: "ChatModel",
        position: { x: 800, y: 200 },
        data: {
          label: "Chat Model",
          display_name: "AI Assistant",
          template: {
            provider: {
              display_name: "Provider",
              type: "options",
              options: ["OpenAI", "Anthropic"],
              value: "OpenAI"
            },
            model: {
              display_name: "Model Name",
              type: "string",
              value: "gpt-4o-mini"
            },
            api_key: {
              display_name: "API Key",
              type: "SecretStr",
              required: !0,
              env_var: "OPENAI_API_KEY"
            },
            system_prompt: {
              display_name: "System Prompt (Optional)",
              type: "string",
              value: "You are a helpful assistant that answers questions based on the provided context."
            },
            prompt: {
              display_name: "Prompt",
              type: "string",
              is_handle: !0
            },
            response: {
              display_name: "Response",
              type: "string",
              is_handle: !0
            }
          },
          resources: { cpu: 0.5, memory: "512Mi", gpu: "none" }
        }
      },
      {
        id: "Output-1",
        type: "Output",
        position: { x: 1e3, y: 600 },
        data: {
          label: "Output",
          display_name: "Final Result",
          template: {
            input_data: {
              display_name: "Input Data",
              type: "object",
              is_handle: !0
            }
          },
          resources: { cpu: 0.1, memory: "128Mi", gpu: "none" }
        }
      }
    ],
    edges: [
      {
        id: "e1-3",
        source: "Input-1",
        source_handle: "data",
        target: "RAGQuery-1",
        target_handle: "query"
      },
      {
        id: "e2-3",
        source: "KnowledgeBase-1",
        source_handle: "knowledge_base",
        target: "RAGQuery-1",
        target_handle: "knowledge_base"
      },
      {
        id: "e3-4",
        source: "RAGQuery-1",
        source_handle: "rag_prompt",
        target: "ChatModel-1",
        target_handle: "prompt"
      },
      {
        id: "e4-5",
        source: "ChatModel-1",
        source_handle: "response",
        target: "Output-1",
        target_handle: "input_data"
      }
    ]
  };
  let V = ((a = o == null ? void 0 : o.nodes) === null || a === void 0 ? void 0 : a.length) > 0 ? [...o.nodes] : K.nodes, B = ((n = o == null ? void 0 : o.edges) === null || n === void 0 ? void 0 : n.length) > 0 ? [...o.edges] : K.edges;
  o != null && o.workflow_name && (ae = o.workflow_name), o != null && o.workflow_id && o.workflow_id;
  const _e = {
    "Input/Output": {
      icon: "📥",
      components: {
        ChatInput: {
          label: "Chat Input",
          icon: "💬",
          color: "#4CAF50",
          defaultData: {
            display_name: "Chat Input",
            template: {
              input_value: {
                display_name: "User Message",
                type: "string",
                value: "",
                is_handle: !0
              }
            },
            resources: { cpu: 0.1, memory: "128Mi", gpu: "none" }
          }
        },
        ChatOutput: {
          label: "Chat Output",
          icon: "💭",
          color: "#F44336",
          defaultData: {
            display_name: "Chat Output",
            template: {
              response: {
                display_name: "AI Response",
                type: "string",
                is_handle: !0
              }
            },
            resources: { cpu: 0.1, memory: "128Mi", gpu: "none" }
          }
        },
        Input: {
          label: "Input",
          icon: "📥",
          color: "#2196F3",
          defaultData: {
            display_name: "Source Data",
            template: {
              data_type: {
                display_name: "Data Type",
                type: "options",
                options: ["string", "image", "video", "audio", "file"],
                value: "string"
              },
              value: {
                display_name: "Value or Path",
                type: "string",
                value: "This is the initial text."
              },
              data: {
                display_name: "Output Data",
                type: "object",
                is_handle: !0
              }
            },
            resources: { cpu: 0.1, memory: "128Mi", gpu: "none" }
          }
        },
        Output: {
          label: "Output",
          icon: "📤",
          color: "#FF9800",
          defaultData: {
            display_name: "Final Result",
            template: {
              input_data: {
                display_name: "Input Data",
                type: "object",
                is_handle: !0
              }
            },
            resources: { cpu: 0.1, memory: "128Mi", gpu: "none" }
          }
        }
      }
    },
    "AI & Language": {
      icon: "🤖",
      components: {
        OpenAIModel: {
          label: "OpenAI Model",
          icon: "🎯",
          color: "#9C27B0",
          defaultData: {
            display_name: "OpenAI Model",
            template: {
              model: {
                display_name: "Model",
                type: "options",
                value: "gpt-4",
                options: ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]
              },
              temperature: {
                display_name: "Temperature",
                type: "number",
                value: 0.7,
                min: 0,
                max: 1
              },
              max_tokens: {
                display_name: "Max Tokens",
                type: "number",
                value: 2048,
                min: 1,
                max: 4096
              },
              api_key: {
                display_name: "API Key",
                type: "SecretStr",
                value: "",
                env_var: "OPENAI_API_KEY"
              },
              prompt: {
                display_name: "Prompt",
                type: "string",
                is_handle: !0
              },
              response: {
                display_name: "Response",
                type: "string",
                is_handle: !0
              }
            },
            resources: { cpu: 0.5, memory: "512Mi", gpu: "none" }
          }
        },
        ChatModel: {
          label: "Chat Model",
          icon: "💭",
          color: "#673AB7",
          defaultData: {
            display_name: "Chat Model",
            template: {
              provider: {
                display_name: "Provider",
                type: "options",
                options: ["OpenAI", "Anthropic"],
                value: "OpenAI"
              },
              model: {
                display_name: "Model",
                type: "string",
                value: "gpt-4o-mini"
              },
              api_key: {
                display_name: "API Key",
                type: "SecretStr",
                required: !0,
                env_var: "OPENAI_API_KEY"
              },
              system_prompt: {
                display_name: "System Prompt",
                type: "string",
                value: "You are a helpful assistant."
              },
              prompt: {
                display_name: "Prompt",
                type: "string",
                is_handle: !0
              },
              response: {
                display_name: "Response",
                type: "string",
                is_handle: !0
              }
            },
            resources: { cpu: 0.5, memory: "512Mi", gpu: "none" }
          }
        },
        Prompt: {
          label: "Prompt",
          icon: "📝",
          color: "#3F51B5",
          defaultData: {
            display_name: "Prompt",
            template: {
              prompt_template: {
                display_name: "Template",
                type: "string",
                value: "{{input}}",
                is_handle: !0
              }
            },
            resources: { cpu: 0.1, memory: "128Mi", gpu: "none" }
          }
        },
        HFTextGeneration: {
          label: "HF Text Generation",
          icon: "🤗",
          color: "#E91E63",
          defaultData: {
            display_name: "HF Text Generation",
            template: {
              model: {
                display_name: "Model",
                type: "string",
                value: "gpt2"
              },
              temperature: {
                display_name: "Temperature",
                type: "number",
                value: 0.7,
                min: 0,
                max: 1
              },
              max_tokens: {
                display_name: "Max Tokens",
                type: "number",
                value: 2048,
                min: 1,
                max: 4096
              },
              api_key: {
                display_name: "API Key",
                type: "SecretStr",
                value: "",
                env_var: "HF_API_KEY"
              },
              prompt: {
                display_name: "Prompt",
                type: "string",
                is_handle: !0
              },
              response: {
                display_name: "Response",
                type: "string",
                is_handle: !0
              }
            },
            resources: { cpu: 0.3, memory: "256Mi", gpu: "none" }
          }
        },
        ReActAgent: {
          label: "ReAct Agent",
          icon: "🤖",
          color: "#9C27B0",
          defaultData: {
            display_name: "LlamaIndex ReAct Agent",
            template: {
              tools_input: {
                display_name: "Available Tools",
                type: "list",
                is_handle: !0,
                info: "Connect WebSearch, ExecutePython, APIRequest, and other tool nodes"
              },
              llm_model: {
                display_name: "LLM Model",
                type: "options",
                options: [
                  "gpt-4o",
                  "gpt-4o-mini",
                  "gpt-3.5-turbo",
                  "gpt-4",
                  "gpt-3.5-turbo-16k"
                ],
                value: "gpt-4o-mini"
              },
              api_key: {
                display_name: "OpenAI API Key",
                type: "SecretStr",
                required: !0,
                env_var: "OPENAI_API_KEY"
              },
              system_prompt: {
                display_name: "System Prompt",
                type: "string",
                value: "You are a helpful AI assistant with access to various tools. Use the available tools to answer user questions accurately and efficiently.",
                multiline: !0
              },
              user_query: {
                display_name: "User Query",
                type: "string",
                is_handle: !0
              },
              max_iterations: {
                display_name: "Max Iterations",
                type: "number",
                value: 8
              },
              temperature: {
                display_name: "Temperature",
                type: "number",
                value: 0.1,
                min: 0,
                max: 2,
                step: 0.1
              },
              verbose: {
                display_name: "Verbose Output",
                type: "boolean",
                value: !0
              },
              agent_response: {
                display_name: "Agent Response",
                type: "string",
                is_handle: !0
              }
            },
            resources: { cpu: 0.5, memory: "512Mi", gpu: "none" }
          }
        }
      }
    },
    "API & Web": {
      icon: "🌐",
      components: {
        APIRequest: {
          label: "API Request",
          icon: "🔌",
          color: "#00BCD4",
          defaultData: {
            display_name: "API Request",
            template: {
              url: {
                display_name: "URL",
                type: "string",
                value: ""
              },
              method: {
                display_name: "Method",
                type: "options",
                value: "GET",
                options: ["GET", "POST", "PUT", "DELETE"]
              },
              headers: {
                display_name: "Headers",
                type: "dict",
                value: {}
              },
              body: {
                display_name: "Body",
                type: "string",
                value: ""
              },
              response: {
                display_name: "Response",
                type: "object",
                is_handle: !0
              }
            },
            resources: { cpu: 0.2, memory: "256Mi", gpu: "none" }
          }
        },
        WebSearch: {
          label: "Web Search",
          icon: "🔍",
          color: "#009688",
          defaultData: {
            display_name: "Web Search",
            template: {
              query: {
                display_name: "Query",
                type: "string",
                value: "",
                is_handle: !0
              },
              num_results: {
                display_name: "Number of Results",
                type: "number",
                value: 5,
                min: 1,
                max: 10
              },
              api_key: {
                display_name: "API Key",
                type: "SecretStr",
                value: "",
                env_var: "SERPAPI_KEY"
              },
              results: {
                display_name: "Search Results",
                type: "list",
                is_handle: !0
              }
            },
            resources: { cpu: 0.2, memory: "256Mi", gpu: "none" }
          }
        }
      }
    },
    "Data Processing": {
      icon: "⚙️",
      components: {
        ExecutePython: {
          label: "Execute Python",
          icon: "🐍",
          color: "#FF5722",
          defaultData: {
            display_name: "Execute Python",
            template: {
              code: {
                display_name: "Python Code",
                type: "string",
                value: `def process(input_data):
    return input_data`
              },
              timeout: {
                display_name: "Timeout",
                type: "number",
                value: 30,
                min: 1,
                max: 300
              },
              input_data: {
                display_name: "Input Data",
                type: "object",
                is_handle: !0
              },
              output_data: {
                display_name: "Output Data",
                type: "object",
                is_handle: !0
              }
            },
            resources: { cpu: 0.3, memory: "256Mi", gpu: "none" }
          }
        },
        ConditionalLogic: {
          label: "Conditional Logic",
          icon: "🔀",
          color: "#795548",
          defaultData: {
            display_name: "Conditional Logic",
            template: {
              condition: {
                display_name: "Condition",
                type: "string",
                value: "{{input}} == True"
              },
              input: {
                display_name: "Input",
                type: "object",
                is_handle: !0
              },
              true_output: {
                display_name: "True Output",
                type: "object",
                is_handle: !0
              },
              false_output: {
                display_name: "False Output",
                type: "object",
                is_handle: !0
              }
            },
            resources: { cpu: 0.1, memory: "128Mi", gpu: "none" }
          }
        },
        Wait: {
          label: "Wait",
          icon: "⏳",
          color: "#607D8B",
          defaultData: {
            display_name: "Wait",
            template: {
              seconds: {
                display_name: "Seconds",
                type: "number",
                value: 1,
                min: 1,
                max: 3600
              },
              input: {
                display_name: "Input",
                type: "object",
                is_handle: !0
              },
              output: {
                display_name: "Output",
                type: "object",
                is_handle: !0
              }
            },
            resources: { cpu: 0.1, memory: "128Mi", gpu: "none" }
          }
        }
      }
    },
    "RAG & Knowledge": {
      icon: "📚",
      components: {
        KnowledgeBase: {
          label: "Knowledge Base",
          icon: "📖",
          color: "#8BC34A",
          defaultData: {
            display_name: "Knowledge Base",
            template: {
              kb_name: {
                display_name: "Knowledge Base Name",
                type: "string",
                value: ""
              },
              source_type: {
                display_name: "Source Type",
                type: "options",
                options: ["Directory", "URL"],
                value: "Directory"
              },
              path_or_url: {
                display_name: "Path or URL",
                type: "string",
                value: ""
              },
              knowledge_base: {
                display_name: "Knowledge Base",
                type: "object",
                is_handle: !0
              }
            },
            resources: { cpu: 0.2, memory: "512Mi", gpu: "none" }
          }
        },
        RAGQuery: {
          label: "RAG Query",
          icon: "🔎",
          color: "#FFC107",
          defaultData: {
            display_name: "RAG Query",
            template: {
              query: {
                display_name: "Query",
                type: "string",
                is_handle: !0
              },
              knowledge_base: {
                display_name: "Knowledge Base",
                type: "object",
                is_handle: !0
              },
              num_results: {
                display_name: "Number of Results",
                type: "number",
                value: 3,
                min: 1,
                max: 10
              },
              rag_prompt: {
                display_name: "RAG Prompt",
                type: "string",
                is_handle: !0
              }
            },
            resources: { cpu: 0.3, memory: "512Mi", gpu: "none" }
          }
        }
      }
    },
    "Speech & Vision": {
      icon: "👁️",
      components: {
        HFSpeechToText: {
          label: "HF Speech to Text",
          icon: "🎤",
          color: "#9E9E9E",
          defaultData: {
            display_name: "HF Speech to Text",
            template: {
              model: {
                display_name: "Model",
                type: "string",
                value: "facebook/wav2vec2-base-960h"
              },
              api_key: {
                display_name: "API Key",
                type: "SecretStr",
                value: "",
                env_var: "HF_API_KEY"
              },
              audio_input: {
                display_name: "Audio Input",
                type: "file",
                is_handle: !0
              },
              text_output: {
                display_name: "Text Output",
                type: "string",
                is_handle: !0
              }
            },
            resources: {
              cpu: 0.4,
              memory: "512Mi",
              gpu: "optional"
            }
          }
        },
        HFTextToSpeech: {
          label: "HF Text to Speech",
          icon: "🔊",
          color: "#CDDC39",
          defaultData: {
            display_name: "HF Text to Speech",
            template: {
              model: {
                display_name: "Model",
                type: "string",
                value: "facebook/fastspeech2-en-ljspeech"
              },
              api_key: {
                display_name: "API Key",
                type: "SecretStr",
                value: "",
                env_var: "HF_API_KEY"
              },
              text_input: {
                display_name: "Text Input",
                type: "string",
                is_handle: !0
              },
              audio_output: {
                display_name: "Audio Output",
                type: "file",
                is_handle: !0
              }
            },
            resources: {
              cpu: 0.4,
              memory: "512Mi",
              gpu: "optional"
            }
          }
        },
        HFSVisionModel: {
          label: "HF Vision Model",
          icon: "👁️",
          color: "#FF9800",
          defaultData: {
            display_name: "HF Vision Model",
            template: {
              model: {
                display_name: "Model",
                type: "string",
                value: "google/vit-base-patch16-224"
              },
              api_key: {
                display_name: "API Key",
                type: "SecretStr",
                value: "",
                env_var: "HF_API_KEY"
              },
              image_input: {
                display_name: "Image Input",
                type: "file",
                is_handle: !0
              },
              prediction: {
                display_name: "Prediction",
                type: "object",
                is_handle: !0
              }
            },
            resources: {
              cpu: 0.4,
              memory: "512Mi",
              gpu: "required"
            }
          }
        }
      }
    },
    "Image Generation": {
      icon: "🎨",
      components: {
        HFImageGeneration: {
          label: "HF Image Generation",
          icon: "🎨",
          color: "#E91E63",
          defaultData: {
            display_name: "HF Image Generation",
            template: {
              model: {
                display_name: "Model",
                type: "string",
                value: "stabilityai/stable-diffusion-2"
              },
              prompt: {
                display_name: "Prompt",
                type: "string",
                value: "",
                is_handle: !0
              },
              num_images: {
                display_name: "Number of Images",
                type: "number",
                value: 1,
                min: 1,
                max: 4
              },
              api_key: {
                display_name: "API Key",
                type: "SecretStr",
                value: "",
                env_var: "HF_API_KEY"
              },
              images: {
                display_name: "Generated Images",
                type: "list",
                is_handle: !0
              }
            },
            resources: { cpu: 0.5, memory: "1Gi", gpu: "required" }
          }
        },
        NebiusImage: {
          label: "Nebius Image",
          icon: "🖼️",
          color: "#2196F3",
          defaultData: {
            display_name: "Nebius Image",
            template: {
              model: {
                display_name: "Model",
                type: "options",
                options: [
                  "black-forest-labs/flux-dev",
                  "black-forest-labs/flux-schnell",
                  "stability-ai/sdxl"
                ],
                value: "black-forest-labs/flux-dev"
              },
              prompt: {
                display_name: "Prompt",
                type: "string",
                value: "",
                is_handle: !0
              },
              negative_prompt: {
                display_name: "Negative Prompt",
                type: "string",
                value: ""
              },
              width: {
                display_name: "Width",
                type: "number",
                value: 1024
              },
              height: {
                display_name: "Height",
                type: "number",
                value: 1024
              },
              num_inference_steps: {
                display_name: "Inference Steps",
                type: "number",
                value: 28
              },
              seed: {
                display_name: "Seed",
                type: "number",
                value: -1
              },
              api_key: {
                display_name: "API Key",
                type: "SecretStr",
                value: "",
                env_var: "NEBIUS_API_KEY"
              },
              image: {
                display_name: "Generated Image",
                type: "file",
                is_handle: !0
              }
            },
            resources: { cpu: 0.5, memory: "1Gi", gpu: "required" }
          }
        }
      }
    },
    "MCP Integration": {
      icon: "🤝",
      components: {
        MCPConnection: {
          label: "MCP Connection",
          icon: "🔌",
          color: "#673AB7",
          defaultData: {
            display_name: "MCP Connection",
            template: {
              server_url: {
                display_name: "Server URL",
                type: "string",
                value: ""
              },
              connection_type: {
                display_name: "Connection Type",
                type: "options",
                options: ["http", "stdio"],
                value: "http"
              },
              allowed_tools: {
                display_name: "Allowed Tools",
                type: "string",
                value: ""
              },
              api_key: {
                display_name: "API Key",
                type: "SecretStr",
                value: "",
                env_var: "MCP_API_KEY"
              },
              connection: {
                display_name: "MCP Connection",
                type: "object",
                is_handle: !0
              }
            },
            resources: { cpu: 0.2, memory: "256Mi", gpu: "none" }
          }
        },
        MCPAgent: {
          label: "MCP Agent",
          icon: "🤖",
          color: "#3F51B5",
          defaultData: {
            display_name: "MCP Agent",
            template: {
              llm_model: {
                display_name: "LLM Model",
                type: "options",
                options: [
                  "gpt-4o",
                  "gpt-4o-mini",
                  "gpt-3.5-turbo",
                  "gpt-4",
                  "gpt-3.5-turbo-16k"
                ],
                value: "gpt-4o"
              },
              api_key: {
                display_name: "OpenAI API Key",
                type: "SecretStr",
                required: !0,
                env_var: "OPENAI_API_KEY"
              },
              system_prompt: {
                display_name: "System Prompt",
                type: "string",
                value: "You are a helpful AI assistant.",
                multiline: !0
              },
              max_iterations: {
                display_name: "Max Iterations",
                type: "number",
                value: 10,
                min: 1,
                max: 20
              },
              temperature: {
                display_name: "Temperature",
                type: "number",
                value: 0.1,
                min: 0,
                max: 2,
                step: 0.1
              },
              verbose: {
                display_name: "Verbose Output",
                type: "boolean",
                value: !1
              },
              user_query: {
                display_name: "User Query",
                type: "string",
                is_handle: !0
              },
              mcp_connection: {
                display_name: "MCP Connection",
                type: "object",
                is_handle: !0
              },
              agent_response: {
                display_name: "Agent Response",
                type: "string",
                is_handle: !0
              }
            },
            resources: { cpu: 0.5, memory: "512Mi", gpu: "none" }
          }
        }
      }
    }
  }, Me = {
    // Input/Output nodes
    ChatInput: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.input_value.display_name",
        label: "Input Field Label",
        type: "text",
        help: "Label shown in the chat input field"
      },
      {
        key: "template.input_value.value",
        label: "Default Message",
        type: "textarea",
        help: "Default message shown in the input field"
      }
    ],
    ChatOutput: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.response.display_name",
        label: "Response Field Label",
        type: "text",
        help: "Label shown in the chat output field"
      }
    ],
    Input: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.data_type.value",
        label: "Data Type",
        type: "select",
        options: ["string", "image", "video", "audio", "file"],
        help: "Type of data this node will handle"
      },
      {
        key: "template.value.value",
        label: "Default Value",
        type: "textarea",
        help: "Default value or path"
      }
    ],
    Output: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      }
    ],
    // AI & Language nodes
    OpenAIModel: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.model.value",
        label: "Model",
        type: "select",
        options: ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]
      },
      {
        key: "template.temperature.value",
        label: "Temperature",
        type: "number",
        min: 0,
        max: 1,
        step: 0.1
      },
      {
        key: "template.max_tokens.value",
        label: "Max Tokens",
        type: "number",
        min: 1,
        max: 4096
      }
    ],
    ChatModel: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.provider.value",
        label: "Provider",
        type: "select",
        options: ["OpenAI", "Anthropic"],
        help: "AI model provider"
      },
      {
        key: "template.model.value",
        label: "Model",
        type: "text",
        help: "Model name"
      },
      {
        key: "template.system_prompt.value",
        label: "System Prompt",
        type: "textarea",
        help: "Optional system prompt"
      }
    ],
    Prompt: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.prompt_template.value",
        label: "Prompt Template",
        type: "textarea",
        help: "Prompt template"
      }
    ],
    HFTextGeneration: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.model.value",
        label: "Model",
        type: "text",
        help: "Model name"
      },
      {
        key: "template.temperature.value",
        label: "Temperature",
        type: "number",
        min: 0,
        max: 1,
        step: 0.1,
        help: "Model temperature"
      },
      {
        key: "template.max_tokens.value",
        label: "Max Tokens",
        type: "number",
        min: 1,
        max: 4096,
        help: "Maximum tokens"
      }
    ],
    ReActAgent: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.llm_model.value",
        label: "LLM Model",
        type: "select",
        options: ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo", "gpt-4", "gpt-3.5-turbo-16k"],
        help: "Model to use for the agent"
      },
      {
        key: "template.system_prompt.value",
        label: "System Prompt",
        type: "textarea",
        help: "System prompt for the agent",
        multiline: !0
      },
      {
        key: "template.max_iterations.value",
        label: "Max Iterations",
        type: "number",
        min: 1,
        max: 20,
        help: "Maximum number of agent iterations"
      },
      {
        key: "template.temperature.value",
        label: "Temperature",
        type: "number",
        min: 0,
        max: 2,
        step: 0.1,
        help: "Model temperature (0-2)"
      },
      {
        key: "template.verbose.value",
        label: "Verbose Output",
        type: "checkbox",
        help: "Show detailed agent reasoning"
      }
    ],
    // API & Web nodes
    APIRequest: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.url.value",
        label: "URL",
        type: "text",
        help: "API endpoint URL"
      },
      {
        key: "template.method.value",
        label: "Method",
        type: "select",
        options: ["GET", "POST", "PUT", "DELETE"],
        help: "HTTP method"
      }
    ],
    WebSearch: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.num_results.value",
        label: "Number of Results",
        type: "number",
        help: "Number of search results"
      }
    ],
    // Data Processing nodes
    ExecutePython: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.code.value",
        label: "Python Code",
        type: "textarea",
        help: "Python code to execute"
      },
      {
        key: "template.timeout.value",
        label: "Timeout",
        type: "number",
        help: "Execution timeout"
      }
    ],
    ConditionalLogic: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.condition.value",
        label: "Condition",
        type: "text",
        help: "Condition expression"
      }
    ],
    Wait: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.seconds.value",
        label: "Seconds",
        type: "number",
        help: "Wait time in seconds"
      }
    ],
    // RAG nodes
    KnowledgeBase: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.kb_name.value",
        label: "Knowledge Base Name",
        type: "text",
        help: "Name for the knowledge base"
      },
      {
        key: "template.source_type.value",
        label: "Source Type",
        type: "select",
        options: ["Directory", "URL"],
        help: "Type of source"
      },
      {
        key: "template.path_or_url.value",
        label: "Path or URL",
        type: "text",
        help: "Source location"
      }
    ],
    RAGQuery: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.num_results.value",
        label: "Number of Results",
        type: "number",
        help: "Number of results to retrieve"
      }
    ],
    // Speech & Vision nodes
    HFSpeechToText: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.model.value",
        label: "Model",
        type: "text",
        help: "HuggingFace model ID"
      }
    ],
    HFTextToSpeech: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.model.value",
        label: "Model",
        type: "text",
        help: "HuggingFace model ID"
      }
    ],
    HFSVisionModel: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.model.value",
        label: "Model",
        type: "text",
        help: "HuggingFace model ID"
      }
    ],
    // Image Generation nodes
    HFImageGeneration: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.model.value",
        label: "Model",
        type: "text",
        help: "HuggingFace model ID"
      },
      {
        key: "template.num_images.value",
        label: "Number of Images",
        type: "number",
        help: "Number of images to generate"
      }
    ],
    NebiusImage: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.model.value",
        label: "Model",
        type: "select",
        options: [
          "black-forest-labs/flux-dev",
          "black-forest-labs/flux-schnell",
          "stability-ai/sdxl"
        ],
        help: "Nebius model to use"
      },
      {
        key: "template.width.value",
        label: "Width",
        type: "number",
        help: "Image width"
      },
      {
        key: "template.height.value",
        label: "Height",
        type: "number",
        help: "Image height"
      },
      {
        key: "template.num_inference_steps.value",
        label: "Inference Steps",
        type: "number",
        help: "Number of inference steps"
      },
      {
        key: "template.seed.value",
        label: "Seed",
        type: "number",
        help: "Random seed (-1 for random)"
      }
    ],
    // MCP nodes
    MCPConnection: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.server_url.value",
        label: "Server URL",
        type: "text",
        help: "MCP server URL"
      },
      {
        key: "template.connection_type.value",
        label: "Connection Type",
        type: "select",
        options: ["http", "stdio"],
        help: "Connection type"
      },
      {
        key: "template.allowed_tools.value",
        label: "Allowed Tools",
        type: "text",
        help: "Optional list of allowed tools"
      }
    ],
    MCPAgent: [
      {
        key: "display_name",
        label: "Display Name",
        type: "text",
        help: "Name shown in the workflow"
      },
      {
        key: "template.llm_model.value",
        label: "LLM Model",
        type: "select",
        options: ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo", "gpt-4", "gpt-3.5-turbo-16k"],
        help: "Model to use for the agent"
      },
      {
        key: "template.system_prompt.value",
        label: "System Prompt",
        type: "textarea",
        help: "System prompt for the agent",
        multiline: !0
      },
      {
        key: "template.max_iterations.value",
        label: "Max Iterations",
        type: "number",
        min: 1,
        max: 20,
        help: "Maximum number of agent iterations"
      },
      {
        key: "template.temperature.value",
        label: "Temperature",
        type: "number",
        min: 0,
        max: 2,
        step: 0.1,
        help: "Model temperature (0-2)"
      },
      {
        key: "template.verbose.value",
        label: "Verbose Output",
        type: "checkbox",
        help: "Show detailed agent reasoning"
      }
    ]
  };
  function Oe() {
    l(4, V = []), l(5, B = []), l(11, S = null), l(14, ae = "My Workflow");
  }
  function je() {
    l(15, O = Math.min(O * 1.2, 3));
  }
  function et() {
    l(15, O = Math.max(O / 1.2, 0.3));
  }
  function De() {
    l(15, O = 1), l(16, j = { x: 0, y: 0 });
  }
  function tt(r) {
    if (r.preventDefault(), r.ctrlKey || r.metaKey) {
      const f = r.deltaY > 0 ? 0.9 : 1.1;
      l(15, O = Math.max(0.3, Math.min(3, O * f)));
    } else
      l(16, j.x -= r.deltaX * 0.5, j), l(16, j.y -= r.deltaY * 0.5, j), l(16, j = Object.assign({}, j));
  }
  function Re(r) {
    (r.button === 1 || r.button === 0 && r.altKey) && (Ee = !0, L = { x: r.clientX, y: r.clientY }, r.preventDefault());
  }
  function Be(r) {
    if (Ee) {
      const f = r.clientX - L.x, F = r.clientY - L.y;
      l(16, j.x += f, j), l(16, j.y += F, j), l(16, j = Object.assign({}, j)), L = { x: r.clientX, y: r.clientY };
    }
  }
  function lt() {
    Ee = !1;
  }
  function ye(r, f, F) {
    r.dataTransfer && (r.dataTransfer.setData("application/json", JSON.stringify({ type: f, data: F })), D = !0);
  }
  function pt(r) {
    var f;
    if (r.preventDefault(), !D) return;
    const F = h.getBoundingClientRect(), z = (r.clientX - F.left - j.x) / O, J = (r.clientY - F.top - j.y) / O;
    try {
      const te = JSON.parse(((f = r.dataTransfer) === null || f === void 0 ? void 0 : f.getData("application/json")) || "{}");
      if (te.type && te.data) {
        const he = {
          id: `${te.type}-${Date.now()}`,
          type: te.type,
          position: {
            x: Math.max(20, z - 160),
            y: Math.max(20, J - 80)
          },
          data: Object.assign(Object.assign({}, te.data.defaultData), { label: te.data.label })
        };
        l(4, V = [...V, he]);
      }
    } catch (te) {
      console.error("Failed to parse drop data:", te);
    }
    D = !1;
  }
  function He(r, f) {
    if (r.target.closest(".node-property") || r.target.closest(".property-input") || r.target.closest(".property-select") || r.target.closest(".property-checkbox") || r.button !== 0) return;
    E = !0, A = f;
    const F = h.getBoundingClientRect(), z = f.position.x * O + j.x, J = f.position.y * O + j.y;
    C.x = r.clientX - F.left - z, C.y = r.clientY - F.top - J, r.preventDefault(), r.stopPropagation();
  }
  function we(r, f) {
    r.stopPropagation(), l(11, S = Object.assign({}, f));
  }
  function q(r) {
    const f = h.getBoundingClientRect();
    if (l(10, Z.x = (r.clientX - f.left - j.x) / O, Z), l(10, Z.y = (r.clientY - f.top - j.y) / O, Z), E && A) {
      const F = V.findIndex((z) => z.id === A.id);
      if (F >= 0) {
        const z = Math.max(0, (r.clientX - f.left - C.x - j.x) / O), J = Math.max(0, (r.clientY - f.top - C.y - j.y) / O);
        l(4, V[F].position.x = z, V), l(4, V[F].position.y = J, V), l(4, V = [...V]), (S == null ? void 0 : S.id) === A.id && l(11, S = Object.assign({}, V[F]));
      }
    }
    Be(r);
  }
  function Ne() {
    E = !1, A = null, l(8, oe = !1), l(9, Q = null), lt();
  }
  function Ce(r, f) {
    r.stopPropagation(), l(8, oe = !0), l(9, Q = f);
  }
  function re(r, f) {
    if (r.stopPropagation(), oe && Q && Q !== f && !B.find((z) => z.source === Q && z.target === f || z.source === f && z.target === Q)) {
      const z = {
        id: `e-${Q}-${f}-${Date.now()}`,
        source: Q,
        target: f
      };
      l(5, B = [...B, z]);
    }
    l(8, oe = !1), l(9, Q = null);
  }
  function pe(r) {
    l(4, V = V.filter((f) => f.id !== r)), l(5, B = B.filter((f) => f.source !== r && f.target !== r)), (S == null ? void 0 : S.id) === r && l(11, S = null);
  }
  function Ue(r) {
    l(5, B = B.filter((f) => f.id !== r));
  }
  function ie(r, f, F) {
    const z = V.findIndex((J) => J.id === r);
    if (z >= 0) {
      const J = f.split(".");
      let te = V[z].data;
      for (let he = 0; he < J.length - 1; he++)
        te[J[he]] || (te[J[he]] = {}), te = te[J[he]];
      te[J[J.length - 1]] = F, l(4, V = [...V]), (S == null ? void 0 : S.id) === r && l(11, S = Object.assign({}, V[z]));
    }
  }
  function at() {
    l(12, fe = !fe);
  }
  function ue() {
    l(13, ve = !ve);
  }
  function ut(r) {
    for (const f of Object.values(_e))
      if (f.components[r])
        return f.components[r];
    return { label: r, icon: "⚡", color: "#6b7280" };
  }
  ol(() => (document.addEventListener("mousemove", q), document.addEventListener("mouseup", Ne), () => {
    document.removeEventListener("mousemove", q), document.removeEventListener("mouseup", Ne);
  }));
  function nt(r) {
    rt.call(this, t, r);
  }
  function me(r) {
    rt.call(this, t, r);
  }
  function ge(r) {
    rt.call(this, t, r);
  }
  function Xe(r) {
    rt.call(this, t, r);
  }
  function be(r) {
    rt.call(this, t, r);
  }
  const Ye = (r, f, F) => ye(F, r, f);
  function Ge() {
    ae = this.value, l(14, ae);
  }
  const qe = (r) => Ue(r.id), st = (r) => Ue(r.id), We = (r, f) => f.id === r.source, ot = (r, f) => f.id === r.target, ct = (r) => pe(r.id), ne = (r, f, F) => ie(r.id, f.key, F.target.value), x = (r, f, F) => ie(r.id, f.key, Number(F.target.value)), Qe = (r, f, F) => ie(r.id, f.key, F.target.checked), dt = (r, f, F) => ie(r.id, f.key, F.target.value), $ = (r, f, F) => ie(r.id, f.key, F.target.value), ze = (r, f, F) => r.type === "object" && re(F, f.id), _t = (r, f, F) => (r.type === "string" || r.type === "list" || r.type === "file") && Ce(F, f.id), se = (r, f) => re(f, r.id), ee = (r, f) => Ce(f, r.id), w = (r, f) => re(f, r.id), M = (r, f) => Ce(f, r.id), H = (r, f) => He(f, r), Je = (r, f) => we(f, r);
  function Ze(r) {
    It[r ? "unshift" : "push"](() => {
      h = r, l(6, h);
    });
  }
  const mt = () => {
    l(11, S = null);
  };
  function xe(r) {
    It[r ? "unshift" : "push"](() => {
      I = r, l(7, I);
    });
  }
  const Ae = (r, f) => ie(S.id, r.key, f.target.value), yt = (r, f) => ie(S.id, r.key, Number(f.target.value)), ht = (r, f) => ie(S.id, r.key, f.target.checked), Ie = (r, f) => ie(S.id, r.key, f.target.value), it = (r, f) => ie(S.id, r.key, f.target.value);
  return t.$$set = (r) => {
    "value" in r && l(37, o = r.value), "elem_id" in r && l(0, s = r.elem_id), "elem_classes" in r && l(1, p = r.elem_classes), "visible" in r && l(2, u = r.visible), "min_width" in r && l(3, _ = r.min_width);
  }, t.$$.update = () => {
    if (t.$$.dirty[1] & /*value*/
    64 && (!o || !o.nodes || o.nodes.length === 0) && l(37, o = K), t.$$.dirty[0] & /*nodes, edges*/
    48 | t.$$.dirty[1] & /*value*/
    64) {
      const r = { nodes: V, edges: B };
      JSON.stringify(r) !== JSON.stringify(o) && (l(37, o = r), g("change", r));
    }
  }, [
    s,
    p,
    u,
    _,
    V,
    B,
    h,
    I,
    oe,
    Q,
    Z,
    S,
    fe,
    ve,
    ae,
    O,
    j,
    _e,
    Me,
    Oe,
    je,
    et,
    De,
    tt,
    Re,
    ye,
    pt,
    He,
    we,
    Ce,
    re,
    pe,
    Ue,
    ie,
    at,
    ue,
    ut,
    o,
    d,
    c,
    v,
    nt,
    me,
    ge,
    Xe,
    be,
    Ye,
    Ge,
    qe,
    st,
    We,
    ot,
    ct,
    ne,
    x,
    Qe,
    dt,
    $,
    ze,
    _t,
    se,
    ee,
    w,
    M,
    H,
    Je,
    Ze,
    mt,
    xe,
    Ae,
    yt,
    ht,
    Ie,
    it
  ];
}
class Ml extends ll {
  constructor(e) {
    super(), al(
      this,
      e,
      Dl,
      Il,
      nl,
      {
        value: 37,
        elem_id: 0,
        elem_classes: 1,
        visible: 2,
        container: 38,
        scale: 39,
        min_width: 3,
        gradio: 40
      },
      null,
      [-1, -1, -1, -1, -1]
    );
  }
  get container() {
    return this.$$.ctx[38];
  }
  get scale() {
    return this.$$.ctx[39];
  }
  get gradio() {
    return this.$$.ctx[40];
  }
}
export {
  Ml as default
};
