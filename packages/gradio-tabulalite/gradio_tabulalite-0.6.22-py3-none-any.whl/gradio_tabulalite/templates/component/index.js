const {
  SvelteComponent: Ke,
  add_render_callback: Qe,
  append_hydration: r,
  attr: C,
  children: N,
  claim_element: d,
  claim_space: M,
  claim_text: q,
  destroy_each: Oe,
  detach: h,
  element: b,
  empty: Ce,
  ensure_array_like: ce,
  get_svelte_dataset: te,
  init: We,
  insert_hydration: z,
  listen: Q,
  noop: Ae,
  run_all: Xe,
  safe_not_equal: Ze,
  select_option: Be,
  select_value: xe,
  set_data: Ee,
  set_input_value: re,
  space: H,
  text: Y,
  toggle_class: De
} = window.__gradio__svelte__internal, { onMount: $e } = window.__gradio__svelte__internal;
function Re(l, e, t) {
  const i = l.slice();
  return i[35] = e[t], i[37] = t, i;
}
function Ue(l, e, t) {
  const i = l.slice();
  return i[38] = e[t], i;
}
function Me(l, e, t) {
  const i = l.slice();
  return i[41] = e[t], i;
}
function He(l) {
  let e, t = ce(Object.keys(
    /*view*/
    l[6][0]
  )), i = [];
  for (let s = 0; s < t.length; s += 1)
    i[s] = Ye(Me(l, t, s));
  return {
    c() {
      for (let s = 0; s < i.length; s += 1)
        i[s].c();
      e = Ce();
    },
    l(s) {
      for (let n = 0; n < i.length; n += 1)
        i[n].l(s);
      e = Ce();
    },
    m(s, n) {
      for (let a = 0; a < i.length; a += 1)
        i[a] && i[a].m(s, n);
      z(s, e, n);
    },
    p(s, n) {
      if (n[0] & /*toggleSort, view, sort_direction, sort_column*/
      332) {
        t = ce(Object.keys(
          /*view*/
          s[6][0]
        ));
        let a;
        for (a = 0; a < t.length; a += 1) {
          const _ = Me(s, t, a);
          i[a] ? i[a].p(_, n) : (i[a] = Ye(_), i[a].c(), i[a].m(e.parentNode, e));
        }
        for (; a < i.length; a += 1)
          i[a].d(1);
        i.length = t.length;
      }
    },
    d(s) {
      s && h(e), Oe(i, s);
    }
  };
}
function qe(l) {
  let e;
  function t(n, a) {
    if (
      /*sort_direction*/
      n[3] === "asc"
    ) return tt;
    if (
      /*sort_direction*/
      n[3] === "desc"
    ) return et;
  }
  let i = t(l), s = i && i(l);
  return {
    c() {
      s && s.c(), e = Ce();
    },
    l(n) {
      s && s.l(n), e = Ce();
    },
    m(n, a) {
      s && s.m(n, a), z(n, e, a);
    },
    p(n, a) {
      i !== (i = t(n)) && (s && s.d(1), s = i && i(n), s && (s.c(), s.m(e.parentNode, e)));
    },
    d(n) {
      n && h(e), s && s.d(n);
    }
  };
}
function et(l) {
  let e;
  return {
    c() {
      e = Y("🔽");
    },
    l(t) {
      e = q(t, "🔽");
    },
    m(t, i) {
      z(t, e, i);
    },
    d(t) {
      t && h(e);
    }
  };
}
function tt(l) {
  let e;
  return {
    c() {
      e = Y("🔼");
    },
    l(t) {
      e = q(t, "🔼");
    },
    m(t, i) {
      z(t, e, i);
    },
    d(t) {
      t && h(e);
    }
  };
}
function Ye(l) {
  let e, t = (
    /*col*/
    l[41] + ""
  ), i, s, n, a, _, c = (
    /*sort_column*/
    l[2] === /*col*/
    l[41] && qe(l)
  );
  function f() {
    return (
      /*click_handler*/
      l[31](
        /*col*/
        l[41]
      )
    );
  }
  return {
    c() {
      e = b("th"), i = Y(t), s = H(), c && c.c(), n = H(), this.h();
    },
    l(v) {
      e = d(v, "TH", { class: !0 });
      var p = N(e);
      i = q(p, t), s = M(p), c && c.l(p), n = M(p), p.forEach(h), this.h();
    },
    h() {
      C(e, "class", "sortable svelte-1i2aiib");
    },
    m(v, p) {
      z(v, e, p), r(e, i), r(e, s), c && c.m(e, null), r(e, n), a || (_ = Q(e, "click", f), a = !0);
    },
    p(v, p) {
      l = v, p[0] & /*view*/
      64 && t !== (t = /*col*/
      l[41] + "") && Ee(i, t), /*sort_column*/
      l[2] === /*col*/
      l[41] ? c ? c.p(l, p) : (c = qe(l), c.c(), c.m(e, n)) : c && (c.d(1), c = null);
    },
    d(v) {
      v && h(e), c && c.d(), a = !1, _();
    }
  };
}
function ze(l) {
  let e, t = (
    /*cell*/
    l[38] + ""
  ), i;
  return {
    c() {
      e = b("td"), i = Y(t), this.h();
    },
    l(s) {
      e = d(s, "TD", { class: !0 });
      var n = N(e);
      i = q(n, t), n.forEach(h), this.h();
    },
    h() {
      C(e, "class", "svelte-1i2aiib");
    },
    m(s, n) {
      z(s, e, n), r(e, i);
    },
    p(s, n) {
      n[0] & /*view*/
      64 && t !== (t = /*cell*/
      s[38] + "") && Ee(i, t);
    },
    d(s) {
      s && h(e);
    }
  };
}
function Fe(l) {
  let e, t, i, s = ce(Object.values(
    /*row*/
    l[35]
  )), n = [];
  for (let _ = 0; _ < s.length; _ += 1)
    n[_] = ze(Ue(l, s, _));
  function a() {
    return (
      /*click_handler_1*/
      l[32](
        /*index*/
        l[37]
      )
    );
  }
  return {
    c() {
      e = b("tr");
      for (let _ = 0; _ < n.length; _ += 1)
        n[_].c();
      this.h();
    },
    l(_) {
      e = d(_, "TR", { class: !0 });
      var c = N(e);
      for (let f = 0; f < n.length; f += 1)
        n[f].l(c);
      c.forEach(h), this.h();
    },
    h() {
      C(e, "class", "svelte-1i2aiib"), De(
        e,
        "selected",
        /*selected_row_index*/
        l[7] === /*index*/
        l[37] + /*currentPage*/
        (l[4] - 1) * /*rows_per_page*/
        l[0]
      );
    },
    m(_, c) {
      z(_, e, c);
      for (let f = 0; f < n.length; f += 1)
        n[f] && n[f].m(e, null);
      t || (i = Q(e, "click", a), t = !0);
    },
    p(_, c) {
      if (l = _, c[0] & /*view*/
      64) {
        s = ce(Object.values(
          /*row*/
          l[35]
        ));
        let f;
        for (f = 0; f < s.length; f += 1) {
          const v = Ue(l, s, f);
          n[f] ? n[f].p(v, c) : (n[f] = ze(v), n[f].c(), n[f].m(e, null));
        }
        for (; f < n.length; f += 1)
          n[f].d(1);
        n.length = s.length;
      }
      c[0] & /*selected_row_index, currentPage, rows_per_page*/
      145 && De(
        e,
        "selected",
        /*selected_row_index*/
        l[7] === /*index*/
        l[37] + /*currentPage*/
        (l[4] - 1) * /*rows_per_page*/
        l[0]
      );
    },
    d(_) {
      _ && h(e), Oe(n, _), t = !1, i();
    }
  };
}
function Ge(l) {
  let e, t = '<td width="100%" class="svelte-1i2aiib">No data found</td>';
  return {
    c() {
      e = b("tr"), e.innerHTML = t, this.h();
    },
    l(i) {
      e = d(i, "TR", { class: !0, "data-svelte-h": !0 }), te(e) !== "svelte-bn1xnp" && (e.innerHTML = t), this.h();
    },
    h() {
      C(e, "class", "svelte-1i2aiib");
    },
    m(i, s) {
      z(i, e, s);
    },
    d(i) {
      i && h(e);
    }
  };
}
function lt(l) {
  let e, t, i, s, n, a, _ = "5", c, f = "10", v, p = "25", A, Z = "50", B, m, P, F, j, E, V, T, x, D, $, G, L, R, ue, ee, _e, J, fe, le, he, ne, de, U, o, K, I, g, W, pe = "📤 Export Current Page as CSV", Te, X, je = "📄 Export Entire Table as CSV", we, ye, y = (
    /*view*/
    l[6].length > 0 && He(l)
  ), ie = ce(
    /*view*/
    l[6]
  ), O = [];
  for (let u = 0; u < ie.length; u += 1)
    O[u] = Fe(Re(l, ie, u));
  let S = (
    /*view*/
    l[6].length === 0 && Ge()
  );
  return {
    c() {
      e = b("div"), t = b("div"), i = b("label"), s = Y(`Rows per page:
      `), n = b("select"), a = b("option"), a.textContent = _, c = b("option"), c.textContent = f, v = b("option"), v.textContent = p, A = b("option"), A.textContent = Z, B = H(), m = b("div"), P = b("input"), F = H(), j = b("div"), E = b("table"), V = b("thead"), T = b("tr"), y && y.c(), x = H(), D = b("tbody");
      for (let u = 0; u < O.length; u += 1)
        O[u].c();
      $ = H(), S && S.c(), G = H(), L = b("div"), R = b("button"), ue = Y("⬅️ Prev"), _e = H(), J = b("span"), fe = Y("Page "), le = Y(
        /*currentPage*/
        l[4]
      ), he = Y(" of "), ne = Y(
        /*totalPages*/
        l[5]
      ), de = H(), U = b("button"), o = Y("Next ➡️"), I = H(), g = b("div"), W = b("button"), W.textContent = pe, Te = H(), X = b("button"), X.textContent = je, this.h();
    },
    l(u) {
      e = d(u, "DIV", { class: !0 });
      var w = N(e);
      t = d(w, "DIV", { class: !0 });
      var k = N(t);
      i = d(k, "LABEL", { class: !0 });
      var se = N(i);
      s = q(se, `Rows per page:
      `), n = d(se, "SELECT", { class: !0 });
      var be = N(n);
      a = d(be, "OPTION", { "data-svelte-h": !0 }), te(a) !== "svelte-1yo0cq6" && (a.textContent = _), c = d(be, "OPTION", { "data-svelte-h": !0 }), te(c) !== "svelte-18d3dpq" && (c.textContent = f), v = d(be, "OPTION", { "data-svelte-h": !0 }), te(v) !== "svelte-1ua5rw2" && (v.textContent = p), A = d(be, "OPTION", { "data-svelte-h": !0 }), te(A) !== "svelte-ujtx1y" && (A.textContent = Z), be.forEach(h), se.forEach(h), k.forEach(h), B = M(w), m = d(w, "DIV", { class: !0 });
      var Pe = N(m);
      P = d(Pe, "INPUT", {
        type: !0,
        placeholder: !0,
        class: !0
      }), Pe.forEach(h), w.forEach(h), F = M(u), j = d(u, "DIV", {});
      var oe = N(j);
      E = d(oe, "TABLE", { class: !0 });
      var me = N(E);
      V = d(me, "THEAD", {});
      var Ie = N(V);
      T = d(Ie, "TR", { class: !0 });
      var Se = N(T);
      y && y.l(Se), Se.forEach(h), Ie.forEach(h), x = M(me), D = d(me, "TBODY", {});
      var ge = N(D);
      for (let Ne = 0; Ne < O.length; Ne += 1)
        O[Ne].l(ge);
      $ = M(ge), S && S.l(ge), ge.forEach(h), me.forEach(h), G = M(oe), L = d(oe, "DIV", { class: !0 });
      var ae = N(L);
      R = d(ae, "BUTTON", { class: !0 });
      var Ve = N(R);
      ue = q(Ve, "⬅️ Prev"), Ve.forEach(h), _e = M(ae), J = d(ae, "SPAN", {});
      var ve = N(J);
      fe = q(ve, "Page "), le = q(
        ve,
        /*currentPage*/
        l[4]
      ), he = q(ve, " of "), ne = q(
        ve,
        /*totalPages*/
        l[5]
      ), ve.forEach(h), de = M(ae), U = d(ae, "BUTTON", { class: !0 });
      var Le = N(U);
      o = q(Le, "Next ➡️"), Le.forEach(h), ae.forEach(h), I = M(oe), g = d(oe, "DIV", { class: !0 });
      var ke = N(g);
      W = d(ke, "BUTTON", { class: !0, "data-svelte-h": !0 }), te(W) !== "svelte-19xlmrj" && (W.textContent = pe), Te = M(ke), X = d(ke, "BUTTON", { class: !0, "data-svelte-h": !0 }), te(X) !== "svelte-84lpb5" && (X.textContent = je), ke.forEach(h), oe.forEach(h), this.h();
    },
    h() {
      a.__value = 5, re(a, a.__value), c.__value = 10, re(c, c.__value), v.__value = 25, re(v, v.__value), A.__value = 50, re(A, A.__value), C(n, "class", "svelte-1i2aiib"), /*rows_per_page*/
      l[0] === void 0 && Qe(() => (
        /*select_change_handler*/
        l[27].call(n)
      )), C(i, "class", "svelte-1i2aiib"), C(t, "class", "toolbar-left svelte-1i2aiib"), C(P, "type", "text"), C(P, "placeholder", "Search..."), C(P, "class", "search-box svelte-1i2aiib"), C(m, "class", "toolbar-right svelte-1i2aiib"), C(e, "class", "toolbar svelte-1i2aiib"), C(T, "class", "svelte-1i2aiib"), C(E, "class", "svelte-1i2aiib"), R.disabled = ee = /*currentPage*/
      l[4] === 1, C(R, "class", "svelte-1i2aiib"), U.disabled = K = /*currentPage*/
      l[4] === /*totalPages*/
      l[5], C(U, "class", "svelte-1i2aiib"), C(L, "class", "controls svelte-1i2aiib"), C(W, "class", "svelte-1i2aiib"), C(X, "class", "svelte-1i2aiib"), C(g, "class", "export-controls svelte-1i2aiib");
    },
    m(u, w) {
      z(u, e, w), r(e, t), r(t, i), r(i, s), r(i, n), r(n, a), r(n, c), r(n, v), r(n, A), Be(
        n,
        /*rows_per_page*/
        l[0],
        !0
      ), r(e, B), r(e, m), r(m, P), re(
        P,
        /*search_term*/
        l[1]
      ), z(u, F, w), z(u, j, w), r(j, E), r(E, V), r(V, T), y && y.m(T, null), r(E, x), r(E, D);
      for (let k = 0; k < O.length; k += 1)
        O[k] && O[k].m(D, null);
      r(D, $), S && S.m(D, null), r(j, G), r(j, L), r(L, R), r(R, ue), r(L, _e), r(L, J), r(J, fe), r(J, le), r(J, he), r(J, ne), r(L, de), r(L, U), r(U, o), r(j, I), r(j, g), r(g, W), r(g, Te), r(g, X), we || (ye = [
        Q(
          n,
          "change",
          /*select_change_handler*/
          l[27]
        ),
        Q(
          n,
          "change",
          /*change_handler*/
          l[28]
        ),
        Q(
          P,
          "input",
          /*input_input_handler*/
          l[29]
        ),
        Q(
          P,
          "input",
          /*input_handler*/
          l[30]
        ),
        Q(
          R,
          "click",
          /*prev*/
          l[14]
        ),
        Q(
          U,
          "click",
          /*next*/
          l[13]
        ),
        Q(
          W,
          "click",
          /*exportCurrentPageAsCSV*/
          l[11]
        ),
        Q(
          X,
          "click",
          /*exportEntireTableAsCSV*/
          l[12]
        )
      ], we = !0);
    },
    p(u, w) {
      if (w[0] & /*rows_per_page*/
      1 && Be(
        n,
        /*rows_per_page*/
        u[0]
      ), w[0] & /*search_term*/
      2 && P.value !== /*search_term*/
      u[1] && re(
        P,
        /*search_term*/
        u[1]
      ), /*view*/
      u[6].length > 0 ? y ? y.p(u, w) : (y = He(u), y.c(), y.m(T, null)) : y && (y.d(1), y = null), w[0] & /*selected_row_index, currentPage, rows_per_page, onRowClick, view*/
      1233) {
        ie = ce(
          /*view*/
          u[6]
        );
        let k;
        for (k = 0; k < ie.length; k += 1) {
          const se = Re(u, ie, k);
          O[k] ? O[k].p(se, w) : (O[k] = Fe(se), O[k].c(), O[k].m(D, $));
        }
        for (; k < O.length; k += 1)
          O[k].d(1);
        O.length = ie.length;
      }
      /*view*/
      u[6].length === 0 ? S || (S = Ge(), S.c(), S.m(D, null)) : S && (S.d(1), S = null), w[0] & /*currentPage*/
      16 && ee !== (ee = /*currentPage*/
      u[4] === 1) && (R.disabled = ee), w[0] & /*currentPage*/
      16 && Ee(
        le,
        /*currentPage*/
        u[4]
      ), w[0] & /*totalPages*/
      32 && Ee(
        ne,
        /*totalPages*/
        u[5]
      ), w[0] & /*currentPage, totalPages*/
      48 && K !== (K = /*currentPage*/
      u[4] === /*totalPages*/
      u[5]) && (U.disabled = K);
    },
    i: Ae,
    o: Ae,
    d(u) {
      u && (h(e), h(F), h(j)), y && y.d(), Oe(O, u), S && S.d(), we = !1, Xe(ye);
    }
  };
}
function Je(l, e) {
  const t = l.map((a) => a.join(",")).join(`
`), i = new Blob([t], { type: "text/csv;charset=utf-8;" }), s = URL.createObjectURL(i), n = document.createElement("a");
  n.setAttribute("href", s), n.setAttribute("download", e), document.body.appendChild(n), n.click(), document.body.removeChild(n);
}
function nt(l, e, t) {
  let { label: i } = e, { visible: s } = e, { elem_id: n } = e, { elem_classes: a } = e, { theme_mode: _ } = e, { target: c } = e, { interactive: f } = e, { server: v } = e, { gradio: p } = e, { root: A } = e, { value: Z = [] } = e, { rows_per_page: B = 10 } = e, m = 1, P = 1, F = [], j = "", E = [], V = null, T = null, x = null, D = null;
  function $(o) {
    V !== o ? (t(2, V = o), t(3, T = "asc")) : T === "asc" ? t(3, T = "desc") : T === "desc" ? (t(2, V = null), t(3, T = null)) : t(3, T = "asc"), t(4, m = 1);
  }
  function G() {
    t(5, P = Math.ceil(E.length / B)), t(4, m = Math.min(Math.max(1, m), P || 1));
    const o = (m - 1) * B;
    t(6, F = E.slice(o, o + B));
  }
  function L(o) {
    t(7, x = o + (m - 1) * B), D = E[x], console.log("Row clicked:", D);
  }
  function R() {
    if (F.length === 0) return;
    const o = [Object.keys(F[0])].concat(F.map((K) => Object.values(K)));
    Je(o, `export_page_${m}.csv`);
  }
  function ue() {
    if (E.length === 0) return;
    const o = [Object.keys(E[0])].concat(E.map((K) => Object.values(K)));
    Je(o, "export_full_table.csv");
  }
  function ee(o) {
    t(4, m = o), G();
  }
  function _e() {
    ee(m + 1);
  }
  function J() {
    ee(m - 1);
  }
  $e(() => G());
  function fe() {
    B = xe(this), t(0, B);
  }
  const le = () => {
    t(4, m = 1), G();
  };
  function he() {
    j = this.value, t(1, j);
  }
  const ne = () => {
    t(4, m = 1), G();
  }, de = (o) => $(o), U = (o) => L(o);
  return l.$$set = (o) => {
    "label" in o && t(15, i = o.label), "visible" in o && t(16, s = o.visible), "elem_id" in o && t(17, n = o.elem_id), "elem_classes" in o && t(18, a = o.elem_classes), "theme_mode" in o && t(19, _ = o.theme_mode), "target" in o && t(20, c = o.target), "interactive" in o && t(21, f = o.interactive), "server" in o && t(22, v = o.server), "gradio" in o && t(23, p = o.gradio), "root" in o && t(24, A = o.root), "value" in o && t(25, Z = o.value), "rows_per_page" in o && t(0, B = o.rows_per_page);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*value, search_term, sort_column, sort_direction*/
    33554446 && t(26, E = Z.filter((o) => Object.values(o).join(" ").toLowerCase().includes(j.toLowerCase())).slice().sort((o, K) => {
      if (!V || !T) return 0;
      let I = o[V], g = K[V];
      return I == null && (I = ""), g == null && (g = ""), !isNaN(Number(I)) && !isNaN(Number(g)) ? (I = Number(I), g = Number(g), T === "asc" ? I - g : g - I) : (I = String(I), g = String(g), T === "asc" ? I.localeCompare(g) : g.localeCompare(I));
    })), l.$$.dirty[0] & /*filtered_value*/
    67108864 && E && E.length >= 0 && G(), l.$$.dirty[0] & /*value*/
    33554432 && Z.length > 0 && t(4, m = 1), l.$$.dirty[0] & /*search_term*/
    2 && j !== "" && t(4, m = 1);
  }, [
    B,
    j,
    V,
    T,
    m,
    P,
    F,
    x,
    $,
    G,
    L,
    R,
    ue,
    _e,
    J,
    i,
    s,
    n,
    a,
    _,
    c,
    f,
    v,
    p,
    A,
    Z,
    E,
    fe,
    le,
    he,
    ne,
    de,
    U
  ];
}
class it extends Ke {
  constructor(e) {
    super(), We(
      this,
      e,
      nt,
      lt,
      Ze,
      {
        label: 15,
        visible: 16,
        elem_id: 17,
        elem_classes: 18,
        theme_mode: 19,
        target: 20,
        interactive: 21,
        server: 22,
        gradio: 23,
        root: 24,
        value: 25,
        rows_per_page: 0
      },
      null,
      [-1, -1]
    );
  }
}
export {
  it as default
};
