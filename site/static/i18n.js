// https://github.com/rehhouari/alpinejs-i18n, modified
(() => {
    var localeChange = new Event("alpine-i18n:locale-change");
    var i18nReady = new Event("alpine-i18n:ready");
    var AlpineI18n = {
      version: "2.3.0-skevo",
      set locale(name) {
        this.currentLocale = name;
        document.dispatchEvent(localeChange);
      },
      get locale() {
        return this.currentLocale;
      },
      currentLocale: "",
      messages: {},
      fallbackLocale: "",
      options: {},
      create(locale, messages, options) {
        this.messages = messages;
        this.locale = locale;
        this.options = options;
      },
      t(name, vars) {
        let message = "";
        try {
          message = name.split(".").reduce((o, i) => o[i], this.messages[this.locale]);
          if (!message)
            throw "";
        } catch {}
        if (!message && this.fallbackLocale.length) {
          message = name.split(".").reduce((o, i) => o[i], this.messages[this.fallbackLocale]);
        } else if (!message) {
          return this.options?.debug ? `???${name}` : name;
        }
        for (const key in vars) {
          if (Object.prototype.hasOwnProperty.call(vars, key)) {
            const val = vars[key];
            let regexp = new RegExp("{s*(" + key + ")s*}", "g");
            message = message.replaceAll(regexp, val);
          }
        }
        return this.options?.debug ? `[${message}]` : message;
      }
    };
    function src_default(Alpine) {
      window.AlpineI18n = Alpine.reactive(AlpineI18n);
      document.dispatchEvent(i18nReady);
      Alpine.magic("locale", (el) => {
        return (locale) => {
          if (!locale)
            return window.AlpineI18n.locale;
          window.AlpineI18n.locale = locale;
        };
      });
      Alpine.magic("t", (_) => {
        return (name, vars) => {
          return window.AlpineI18n.t(name, vars);
        };
      });
    }
  
    document.addEventListener("alpine:initializing", () => {
      src_default(window.Alpine);
    });
  })();