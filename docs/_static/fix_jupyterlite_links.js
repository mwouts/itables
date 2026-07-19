// sphinx-book-theme's "rocket icon" JupyterLite launch button renders its
// href as a path relative to the *site root* (e.g. "lite/lab/index.html?..."),
// but never adjusts it for how deep the current page is nested -- unlike its
// other buttons, it doesn't go through Sphinx's pathto(). So the link is only
// correct on top-level pages; on e.g. apps/widget.html it resolves to
// apps/lite/lab/index.html (a 404) instead of ../lite/lab/index.html.
//
// DOCUMENTATION_OPTIONS.pagename (e.g. "apps/widget") tells us how deep the
// current page is nested, which we use to build the right "../" prefix.
document.addEventListener("DOMContentLoaded", function () {
  var pagename =
    (window.DOCUMENTATION_OPTIONS && window.DOCUMENTATION_OPTIONS.pagename) ||
    "";
  var depth = pagename.split("/").length - 1;
  var root = "../".repeat(depth);
  document.querySelectorAll('a[href^="lite/lab/index.html"]').forEach(
    function (link) {
      link.setAttribute("href", root + link.getAttribute("href"));
    }
  );
});
