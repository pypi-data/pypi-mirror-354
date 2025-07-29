const {
  SvelteComponent: y,
  add_iframe_resize_listener: g,
  add_render_callback: b,
  append_hydration: m,
  attr: v,
  binding_callbacks: p,
  children: w,
  claim_element: z,
  claim_text: E,
  detach: o,
  element: k,
  init: A,
  insert_hydration: S,
  noop: u,
  safe_not_equal: V,
  set_data: j,
  text: q,
  toggle_class: s
} = window.__gradio__svelte__internal, { onMount: C } = window.__gradio__svelte__internal;
function D(t) {
  let e, i, r;
  return {
    c() {
      e = k("div"), i = q(
        /*displayValue*/
        t[4]
      ), this.h();
    },
    l(l) {
      e = z(l, "DIV", { class: !0 });
      var n = w(e);
      i = E(
        n,
        /*displayValue*/
        t[4]
      ), n.forEach(o), this.h();
    },
    h() {
      v(e, "class", "svelte-84cxb8"), b(() => (
        /*div_elementresize_handler*/
        t[6].call(e)
      )), s(
        e,
        "table",
        /*type*/
        t[0] === "table"
      ), s(
        e,
        "gallery",
        /*type*/
        t[0] === "gallery"
      ), s(
        e,
        "selected",
        /*selected*/
        t[1]
      );
    },
    m(l, n) {
      S(l, e, n), m(e, i), r = g(
        e,
        /*div_elementresize_handler*/
        t[6].bind(e)
      ), t[7](e);
    },
    p(l, [n]) {
      n & /*displayValue*/
      16 && j(
        i,
        /*displayValue*/
        l[4]
      ), n & /*type*/
      1 && s(
        e,
        "table",
        /*type*/
        l[0] === "table"
      ), n & /*type*/
      1 && s(
        e,
        "gallery",
        /*type*/
        l[0] === "gallery"
      ), n & /*selected*/
      2 && s(
        e,
        "selected",
        /*selected*/
        l[1]
      );
    },
    i: u,
    o: u,
    d(l) {
      l && o(e), r(), t[7](null);
    }
  };
}
function I(t, e) {
  t.style.setProperty("--local-text-width", `${e && e < 150 ? e : 200}px`), t.style.whiteSpace = "unset";
}
function M(t, e, i) {
  let r, { value: l } = e, { type: n } = e, { selected: c = !1 } = e, _, d;
  C(() => {
    I(d, _);
  });
  function f() {
    _ = this.clientWidth, i(2, _);
  }
  function h(a) {
    p[a ? "unshift" : "push"](() => {
      d = a, i(3, d);
    });
  }
  return t.$$set = (a) => {
    "value" in a && i(5, l = a.value), "type" in a && i(0, n = a.type), "selected" in a && i(1, c = a.selected);
  }, t.$$.update = () => {
    t.$$.dirty & /*value*/
    32 && i(4, r = Array.isArray(l) && l.length > 0 ? l.join(", ") : "Empty list");
  }, [
    n,
    c,
    _,
    d,
    r,
    l,
    f,
    h
  ];
}
class P extends y {
  constructor(e) {
    super(), A(this, e, M, D, V, { value: 5, type: 0, selected: 1 });
  }
}
export {
  P as default
};
