"use strict";

function _inheritsLoose(subClass, superClass) { subClass.prototype = Object.create(superClass.prototype); subClass.prototype.constructor = subClass; subClass.__proto__ = superClass; }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

if (typeof require === 'function') {
  var React = require('react');
}

var Fragment = React.Fragment ||
/*#__PURE__*/
function (_React$Component) {
  _inheritsLoose(_Fragment, _React$Component);

  function _Fragment(props) {
    var _this;

    _this = _React$Component.call(this, props) || this;
    _this.refFn = _this.refFn.bind(_assertThisInitialized(_this));
    _this.orphans = [];
    _this.focusedDescendantElement = null;
    _this.parentNode = null;
    return _this;
  }

  var _proto = _Fragment.prototype;

  _proto.refFn = function refFn(div) {
    this.div = div;
  };

  _proto.componentDidMount = function componentDidMount() {
    this.unwrapChildren();
    this.div.style.display = 'none';
  };

  _proto.componentDidUpdate = function componentDidUpdate() {
    this.unwrapChildren();
  };

  _proto.componentWillUnmount = function componentWillUnmount() {
    this.rewrapChildren();
  };

  _proto.unwrapChildren = function unwrapChildren() {
    var _this2 = this;

    // defer first to style calculation to ensure CSS transitions can happen:
    // https://stackoverflow.com/a/24195559/4956731
    this.unwrapTimeout = setTimeout(function () {
      // plain js rocks!
      // https://plainjs.com/javascript/manipulation/unwrap-a-dom-element-35/
      if (!_this2.div.parentNode) {
        return;
      }

      _this2.saveFocusedDescendantElement(_this2.div);

      _this2.orphans = [];

      while (_this2.div.firstChild) {
        _this2.orphans.push(_this2.div.firstChild);

        _this2.div.parentNode.insertBefore(_this2.div.firstChild, _this2.div);
      }

      _this2.parentNode = _this2.div.parentNode;

      if (_this2.orphans.length) {
        // it's only safe to remove the wrapper div
        // if the fragment has some child dom elements,
        // since otherwise we have no way to remember
        // our position among the sibling elements.
        _this2.parentNode.removeChild(_this2.div);
      }

      _this2.restoreFocusedDescendantElement();
    });
  };

  _proto.rewrapChildren = function rewrapChildren() {
    clearTimeout(this.unwrapTimeout);

    if (!(this.div && this.parentNode && this.parentNode.parentNode)) {
      return;
    }

    if (this.orphans.length) {
      this.parentNode.insertBefore(this.div, this.orphans[0]);
      this.saveFocusedDescendantElement(this.orphans[0].parentNode);
      var orphan;

      while (orphan = this.orphans.shift()) {
        this.div.appendChild(orphan);
      }
    }
  };

  _proto.saveFocusedDescendantElement = function saveFocusedDescendantElement(ancestorElement) {
    if (ancestorElement.contains(document.activeElement)) {
      this.focusedDescendantElement = document.activeElement;
    }
  };

  _proto.restoreFocusedDescendantElement = function restoreFocusedDescendantElement() {
    if (this.focusedDescendantElement) {
      this.focusedDescendantElement.focus();
      this.focusedDescendantElement = null;
    }
  };

  _proto.render = function render() {
    // sorry for the side effects! 😭
    this.rewrapChildren();
    return React.createElement('div', {
      ref: this.refFn
    }, this.props.children);
  };

  return _Fragment;
}(React.Component);

if (typeof module !== 'undefined' && module) {
  module.exports = Fragment;
}
