"use strict";

var gulp = require('gulp');
var browserify = require('browserify'); // Bundles JS
var reactify = require('reactify');  // Transforms React JSX to JS
var source = require('vinyl-source-stream'); // use conventional text streams with Gulp
var concat = require('gulp-concat'); //concatenate files
var uglify = require('gulp-uglify');
var buffer = require('vinyl-buffer');

var config = {
    port: 8000,
    devBaseUrl: 'http://localhost',
    paths: {
        html: './static_src/*.html',
        js: './static_src/**/*.js',
        jsLibs: './static_src/js/libs/*.js',
        css: [
            'node_modules/bootstrap/dist/css/bootstrap.min.css',
            'node_modules/bootstrap/dist/css/bootstrap-theme.min.css',
            './static_src/**/*.css',
        ],
        css_map: [
            'node_modules/bootstrap/dist/css/bootstrap.min.css.map'
        ],
        glyphicons: [
            'node_modules/bootstrap/fonts/glyphicons-halflings-regular.eot',
            'node_modules/bootstrap/fonts/glyphicons-halflings-regular.svg',
            'node_modules/bootstrap/fonts/glyphicons-halflings-regular.ttf',
            'node_modules/bootstrap/fonts/glyphicons-halflings-regular.woff',
            'node_modules/bootstrap/fonts/glyphicons-halflings-regular.woff2'
        ],
        dist: './dist',
        mainJs: './static_src/js/main.js',
        favicon: './static_src/favicon.ico',
    }
}

gulp.task('js', function() {
    browserify(config.paths.mainJs)
        .transform(reactify)
        .bundle()
        .on('error', console.error.bind(console))
        .pipe(source('bundle.js'))
        .pipe(buffer())
        .pipe(uglify())
        .pipe(gulp.dest(config.paths.dist + '/js'));
    gulp.src(config.paths.jsLibs)
        .pipe(gulp.dest(config.paths.dist + '/js'));
});

gulp.task('css', function(){
    gulp.src(config.paths.css)
        .pipe(concat('bundle.css'))
        .pipe(gulp.dest(config.paths.dist + '/css'));
});

gulp.task('glyphicons', function() {
    gulp.src(config.paths.glyphicons)
        .pipe(gulp.dest(config.paths.dist + '/fonts'));
});

gulp.task('css_map', function() {
    gulp.src(config.paths.css_map)
        .pipe(gulp.dest(config.paths.dist + '/css'));
}) ;

gulp.task('favicon', function() {
    gulp.src(config.path.favicon)
        .pipe(gulp.dest(config.paths.dist));
});

gulp.task('watch', function() {
    // gulp.watch(config.paths.html, ['html']);
    gulp.watch(config.paths.js, ['js']);
    gulp.watch(config.paths.css, ['css']);
});

gulp.task('default', ['js', 'watch', 'css', 'css_map', 'glyphicons']);
