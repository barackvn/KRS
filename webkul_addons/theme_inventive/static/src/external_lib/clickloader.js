/* InstantClick 3.1.0 | (C) 2014 Alexandre Dieulot | http://instantclick.io/license */

var InstantClick = function(document, location) {
  // Internal variables
  var $currentLocationWithoutHash = ""

  ////////// HELPERS //////////

  function removeHash(url) {
    var index = url.indexOf('#')
    if (index < 0) {
      return url
    }
    return url.substr(0, index)
  }

  function getLinkTarget(target) {
    while (target && target.nodeName != 'A') {
      target = target.parentNode
    }
    return target
  }

  function isPreloadable(a) {
    var domain = location.protocol + '//' + location.host
    if (a.target // target="_blank" etc.
        || a.hasAttribute('download')
        || a.href.indexOf(domain + '/') != 0 // Another domain, or no href attribute
        || (a.href.indexOf('#') > -1) // Anchor
        || !a.href // Anchor
        || $._data(a, "events")
       ) {
      return false
    }
    return true
  }

  ////////// EVENT HANDLERS //////////

  function click(e) {
    var a = getLinkTarget(e.target)

    if (!a || !isPreloadable(a)) {
      return
    }

    if (e.which > 1 || e.metaKey || e.ctrlKey) { // Opening in new tab
      return
    }
    console.log("Clicked on js");
    var options = {
         theme:"sk-cube-grid",
         message:'some cool message for your user here ! Or where the logo is ! Your skills are the only limit. ',
         backgroundColor:"#555555",
         textColor:"white"
    };
    HoldOn.open(options);
    console.log("HoldOn",HoldOn);
    // e.preventDefault();
  }

  ////////// MAIN FUNCTIONS //////////

  function instantanize() {
    document.body.addEventListener('click', click, true)
  }
  function init() {
    instantanize(true)
  }


  return {
    init: init,
  }

}(document, location);
