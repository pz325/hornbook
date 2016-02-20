var context = require.context('./static_src/js/components', true, /-test\.jsx?$/);
context.keys().forEach(context);