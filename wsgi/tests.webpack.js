var context = require.context('./static/js/components', true, /-test\.jsx?$/);
context.keys().forEach(context);