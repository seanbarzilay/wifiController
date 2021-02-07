<template>
    <div>
        <div class="md-layout md-gutter md-alignment-center">
            <md-button class="md-raised md-layout-item md-size-10" v-on:click="goBack()">Back</md-button>
        </div>
        <div class="md-layout md-alignment-center md-gutter">
            <span v-if="!saved" class="md-headline">*</span>
            <span class="md-headline">{{this.$route.params.file}}</span>
        </div>
        <div class="yaml-editor">
            <textarea ref="textarea"/>
        </div>
        <div class="md-layout md-gutter md-alignment-center">
            <md-button class="md-raised md-primary" v-on:click="saveFile(getValue())">Save</md-button>
        </div>
    </div>
</template>

<script>
    import CodeMirror from 'codemirror'
    import 'codemirror/addon/lint/lint.css'
    import 'codemirror/lib/codemirror.css'
    import 'codemirror/theme/monokai.css'
    import 'codemirror/mode/yaml/yaml'
    import 'codemirror/addon/lint/lint'
    import 'codemirror/addon/lint/yaml-lint'
    import axios from 'axios';

    window.jsyaml = require('js-yaml') // Introduce js-yaml to improve core support for grammar checking for codemirror

    export default {
        name: 'YamlEditor',
        // eslint-disable-next-line vue/require-prop-types
        props: ['value'],
        data() {
            return {
                yamlEditor: false,
                saved: false
            }
        },
        watch: {
            value(value) {
                const editorValue = this.yamlEditor.getValue();
                if (value !== editorValue) {
                    this.yamlEditor.setValue(this.value)
                }
            }
        },
        mounted() {
            axios.get("http://localhost:5000/config/" + this.$route.params.file)
                .then((res) => {
                    const fileContents = res.data.data;
                    this.yamlEditor = CodeMirror.fromTextArea(this.$refs.textarea, {
                        lineNumbers: true, // display line number
                        mode: 'text/x-yaml', // grammar model
                        gutters: ['CodeMirror-lint-markers'],  // Syntax checker
                        theme: 'monokai', // Editor theme
                        lint: true, // Turn on grammar checking
                        smartIndent: true
                    });
                    this.saved = true;

                    this.yamlEditor.setValue(fileContents);
                    this.yamlEditor.on('change', (cm) => {
                        this.saved = false;
                        this.$emit('changed', cm.getValue());
                        this.$emit('input', cm.getValue())
                    })
                })
                .catch((error) => {
                    console.error(error)
                })

        },
        methods: {
            getValue() {
                return this.yamlEditor.getValue()
            },
            saveFile(value) {
                axios.post("http://localhost:5000/config/" + this.$route.params.file, {text: value})
                    .then((res) => {
                        console.info(res);
                        this.saved = true
                    }).catch((error) => {
                    console.error(error)
                })
            },
            goBack() {
                this.$router.go(-1)
            }
        }
    }
</script>

<style scoped>
    .yaml-editor {
        height: 100%;
        position: relative;
    }

    .yaml-editor >>> .CodeMirror {
        height: auto;
        min-height: 300px;
    }

    .yaml-editor >>> .CodeMirror-scroll {
        min-height: 300px;
    }

    .yaml-editor >>> .cm-s-rubyblue span.cm-string {
        color: #F08047;
    }
</style>
