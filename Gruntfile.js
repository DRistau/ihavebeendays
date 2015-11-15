module.exports = function(grunt) {
    var config = {
        pkg: grunt.file.readJSON('package.json'),
        appPath: 'ihavebeendays',
        staticPath: '<%= appPath %>/static'
    };

    config.autoprefixer = {
        no_dest_single: {
            src: '<%= staticPath %>/css/styles.css',
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

    config.watch = {
        options: {
            livereload: true
        },
        sass: {
            files: ['<%= staticPath %>/sass/**/*.{scss,sass}', '<%= staticPath %>/sass/partials/**/*.{scss,sass}'],
            tasks: ['sass:dist', 'uglify:dist', 'autoprefixer']
        }
    };

    grunt.initConfig(config);

    grunt.loadNpmTasks('grunt-autoprefixer');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-sass');

    grunt.registerTask('default', ['sass', 'cssmin', 'autoprefixer', 'watch:sass']);
};
