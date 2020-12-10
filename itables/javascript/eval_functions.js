function eval_functions(map_or_text) {
    if (typeof map_or_text === "string") {
        if (map_or_text.startsWith("function")) {
            try {
                // Note: parenthesis are required around the whole expression for eval to return a value!
                // See https://stackoverflow.com/a/7399078/911298.
                //
                // eval("local_fun = " + map_or_text) would fail because local_fun is not declared
                // (using var, let or const would work, but it would only be declared in the local scope
                // and therefore the value could not be retrieved).
                const func = eval("(" + map_or_text + ")");
                if (typeof func !== "function") {
                    // Note: backquotes are super convenient!
                    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals
                    console.error("Evaluated expression " + map_or_text + " is not a function (type is " + typeof func + ")");
                    return map_or_text;
                }
                // Return the function
                return func;
            } catch (e) {
                // Make sure to print the error with a second argument to console.error().
                console.error("itables was not able to parse " + map_or_text, e);
            }
        }
    } else if (typeof map_or_text === "object") {
        if (map_or_text instanceof Array) {
            // Note: "var" is now superseded by "let" and "const".
            // https://medium.com/javascript-scene/javascript-es6-var-let-or-const-ba58b8dcde75
            const result = [];
            // Note: "for of" is the best way to iterate through an iterable.
            // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for...of
            for (const item of map_or_text) {
                result.push(eval_functions(item));
            }
            return result;

            // Alternatively, more functional approach in one line:
            // return map_or_text.map(eval_functions);
        } else {
            const result = {};
            // Object.keys() is safer than "for in" because otherwise you might have keys
            // that aren't defined in the object itself.
            //
            // See https://stackoverflow.com/a/684692/911298.
            for (const item of Object.keys(map_or_text)) {
                result[item] = eval_functions(map_or_text[item]);
            }
            return result;
        }
    }

    return map_or_text;
}
