window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, context) {
            const {
                classes,
                colorscale,
                style,
                colorProp
            } = context.hideout;
            const value = feature.properties[colorProp];

            if (typeof value !== 'number') {
                console.warn(`Invalid data type for colorProp: ${colorProp}. Expected a number.`);
                return style;
            }

            for (let i = 0; i < classes.length; ++i) {
                if (value < classes[i + 1]) {
                    style.fillColor = colorscale[i];
                    break; // Exit loop after assigning color
                }
            }
            return style;
        }

    }
});