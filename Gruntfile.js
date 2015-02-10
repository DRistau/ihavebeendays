module.exports = function(grunt) {
    var config = {
        pkg: grunt.file.readJSON('package.json'),
        appPath: 'ibeendays'
    };

    config.sass = {
        options: {
            sourceMap: true,
            outputStyle: 'expanded'
        },
        dist: {
            files: {
                '<%= appPath %>/static/css/styles.css': '<%= appPath %>/sass/styles.scss'
            }
        }
    };

    config.autoprefixer = {
        no_dest_single: {
            src: '<%= appPath %>/static/css/styles.css',
        }
    };

    config.watch = {
        sass: {
            files: ['<%= appPath %>/sass/**/*.{scss,sass}', '<%= appPath %>/sass/partials/**/*.{scss,sass}'],
            tasks: ['sass:dist', 'autoprefixer']
        }
    };

    grunt.initConfig(config);

    grunt.loadNpmTasks('grunt-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-autoprefixer');

    grunt.registerTask('default', ['sass', 'autoprefixer', 'watch:sass']);
};
