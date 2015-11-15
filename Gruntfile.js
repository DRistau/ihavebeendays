module.exports = function(grunt) {
    var autoprefixer = require('autoprefixer'),
        pixrem = require('pixrem');

    var config = {
        pkg: grunt.file.readJSON('package.json'),
        appPath: 'ihavebeendays',
        staticPath: '<%= appPath %>/static'
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

    config.watch = {
        options: {
            livereload: true
        },
        sass: {
            files: ['<%= staticPath %>/sass/**/*.{scss,sass}', '<%= staticPath %>/sass/partials/**/*.{scss,sass}'],
            tasks: ['sass:dist', 'postcss', 'cssmin']
        }
    };

    grunt.initConfig(config);

    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-postcss');
    grunt.loadNpmTasks('grunt-sass');

    grunt.registerTask('default', ['sass', 'postcss', 'cssmin', 'watch:sass']);
};
