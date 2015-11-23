module.exports = function(grunt) {
    var autoprefixer = require('autoprefixer'),
        pixrem = require('pixrem');

    var config = {
        pkg: grunt.file.readJSON('package.json'),
        appPath: 'ihavebeendays',
        staticPath: '<%= appPath %>/static'
    };

    config.browserify = {
        dist: {
            options: {
                transform: [
                    ['babelify', {presets: ['es2015', 'react']}]
                ]
            },
            files: {
                '<%= staticPath %>/js/dist/main.js': [
                    '<%= staticPath %>/js/src/index.js'
                ]
            }
        }
    };

    config.concurrent = {
        watch: ['watch:sass', 'watch:scripts']
    };

    config.cssmin = {
        options: {
            sourceMap: true
        },
        target: {
            files: {
                '<%= staticPath %>/css/styles.min.css': [
                    '<%= staticPath %>/vendor/*.css',
                    '<%= staticPath %>/css/styles.css'
                ]
            }
        }
    };

    config.postcss = {
        options: {
            processors: [
                pixrem(),
                autoprefixer({
                    browsers: 'last 2 versions'
                })
            ]
        },
        dist: {
            src: '<%= staticPath %>/css/styles.css'
        }
    };

    config.sass = {
        options: {
            sourceMap: true,
            outputStyle: 'expanded'
        },
        dist: {
            files: {
                '<%= staticPath %>/css/styles.css': '<%= staticPath %>/sass/styles.scss'
            }
        }
    };

    config.watch = {
        sass: {
            options: {
                livereload: true
            },
            files: ['<%= staticPath %>/sass/**/*.{scss,sass}', '<%= staticPath %>/sass/partials/**/*.{scss,sass}'],
            tasks: ['sass:dist', 'postcss', 'cssmin']
        },
        scripts: {
            files: ['<%= staticPath %>/js/src/*.js', '<%= staticPath %>/js/src/**/*.{js,jsx}'],
            tasks: ['browserify']
        }
    };

    grunt.initConfig(config);

    grunt.loadNpmTasks('grunt-browserify');
    grunt.loadNpmTasks('grunt-concurrent');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-postcss');
    grunt.loadNpmTasks('grunt-sass');

    grunt.registerTask('css', ['sass', 'postcss', 'cssmin']);
    grunt.registerTask('js', ['browserify']);
    grunt.registerTask('default', ['css', 'js', 'concurrent:watch']);
};
