
// base functions(like python)
function enumerate(source) {
    var enums = [];
    if (typeof(source) == "object") {
        var idx = 0;
        for (var key in source) {
            enums.push([ idx, key, source[key] ]);
            idx += 1;
        }
    }
    else {
        var idx = 0;
        for (var item of source) {
            enums.push([ idx, item ]);
            idx += 1;
        }
    }

    return enums;
}

// base functions(type casts)
function int(source) {
    try {
        return parseInt(source);
    }
    catch {
        return source;
    }
}

function float(source) {
    try {
        return parseFloat(source);
    }
    catch {
        return source;
    }
}

function bool(source) {
    try {
        return Boolean(source);
    }
    catch {
        return source;
    }
}

function str(source) {
    try {
        return toString(source);
    }
    catch {
        return source;
    }
}

function list(source) {
    return source;
}

function dict(source) {
    return source;
}

// decorators
function defineElement(tag_name) {
    return (cls) => {
        window.customElements.define(tag_name, cls);
        Object.defineProperty(cls, "tag_name", {"value": tag_name, "enumerable": false, "configurable": false, "writable": false});

        return cls;
    };
};

// directives
function repeat(iterable, iter_method) {
    var templates = [];
    
    if (typeof(iterable) == "object" && !(iterable instanceof Array) && !(iterable instanceof Date)) {
        // convert to list if dictionary
        var iterable_array = [];
        for (var key of Object.getOwnPropertyNames(iterable)) {
            iterable_array.push([ key, iterable[key] ]);
        }

        iterable = iterable_array;
    }

    for (var iter_item of iterable) {
        try {
            templates.push(iter_method(...iter_item));
        }
        catch {
            templates.push(iter_method(iter_item));
        }
    }

    return templates.join("\n")
};

// core classes
var brue = {
    $route_view: null,
    routes: {},
    store: {},
    use(cls) {
        if (cls["type"] != undefined) {
            var cls_type = cls["type"];
            delete cls["type"];
            if (cls_type == "brueStore") {
                brue.store = cls;
            }
            else if (cls_type == "brueRoute") {
                brue.routes = {};
                for (var item of cls["info"]) {
                    brue.routes[item["path"]] = item["component"].tag_name;
                }
            }
        }
    }
};

function brueStore(kwargs) {
    kwargs["type"] = "brueStore";
    return kwargs;
}

function brueRoute(router_infos) {
    return {
        type: "brueRoute",
        info: router_infos
    };
}

class brueElement extends HTMLElement {
    constructor() {
        super();

        this.created();

        this.store = brue.store;
        this.$props = this.props == undefined ? {} : this.props;
        if (this.state == undefined) {
            this.state = {};
        }

        this.attachShadow({ mode: "open" });
    }

    $find_element_custom_attr(element) {
        var has_custom_attr = false;
        for (var idx = 0; idx < element.attributes.length; idx++) {
            var key = element.attributes[idx].name;
            if (key.startsWith(":")) {
                has_custom_attr = true;
                break;
            }
        }

        if (has_custom_attr) {
            this.$connect_event(element);
        }

        for (var child of element.children) {
            this.$find_element_custom_attr(child);
        }
    }

    $connect_event(element) {
        var self = this;

        for (var idx = 0; idx < element.attributes.length; idx++) {
            var key = element.attributes[idx].name;
            if (key.startsWith(":")) {
                var func = eval(element.attributes[idx].value);
                element.removeAttribute(key);
                element.addEventListener(key.substring(1), func.bind(this));
            }
        }
    }

    connectedCallback() {
        this.mounted();

        var self = this;
        var props = {}, state = {};
        for (var key in this.$props) {
            if (this.hasAttribute(key)) {
                props[key] = this.getAttribute(key);
            }
        }
        this.props = props;

        for (var key in this.state) {
            state[key] = this.state[key];
        }

        this.state = new Proxy(state, {
            get(t, n, r) {
                return Reflect.get(t, n, r);
            },
            set(t, n, r) {
                var res = Reflect.set(t, n, r);
                self.$update();

                return res;
            }
        });

        this.$update();
    }

    $update() {
        this.shadowRoot.innerHTML = this.render();
        if (this.constructor.css_string != undefined) {
            var style_elm = document.createElement("style");
            style_elm.setAttribute("type", "text/css");
            style_elm.appendChild(document.createTextNode(this.constructor.css_string));

            this.shadowRoot.appendChild(style_elm);
        }
        this.$find_element_custom_attr(this.shadowRoot.firstElementChild);
    }

    created() {}

    mounted() {}

    render() {}
};


// custom elements
// routers
class RouterLink extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: "open" });
    }

    connectedCallback() {
        this.$text = this.firstChild.nodeValue;

        this.$url = this.getAttribute("url");
        this.removeAttribute("url");

        var link = document.createElement("a");
        link.href = "#";
        link.innerText = this.firstChild.nodeValue;
        link.addEventListener("click", (ev) => {
            brue.$route_view.change_view(this.$url);
        })
        this.shadowRoot.appendChild(link);
        this.removeChild(this.firstChild);
    }
}
window.customElements.define("router-link", RouterLink);

class RouterView extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: "open" });
        brue.$route_view = this;
    }

    connectedCallback() {
        this.change_view("/");
    }

    change_view(view_url) {
        if (brue.routes.hasOwnProperty(view_url)) {
            var tag_name = brue.routes[view_url];
            var elm = document.createElement(tag_name);

            this.shadowRoot.innerHTML = "";
            this.shadowRoot.appendChild(elm);
        }
    }
}
window.customElements.define("router-view", RouterView);

