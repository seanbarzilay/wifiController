<template>
  <div class="yaml-editor">
    <textarea ref="textarea"/>
    <button v-on:click="test(getValue())">Add 1</button>
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

window.jsyaml = require('js-yaml') // Introduce js-yaml to improve core support for grammar checking for codemirror

export default {
  name: 'YamlEditor',
  // eslint-disable-next-line vue/require-prop-types
  props: ['value'],
  data() {
    return {
      yamlEditor: false
    }
  },
  watch: {
    value(value) {
      const editorValue = this.yamlEditor.getValue()
      if (value !== editorValue) {
        this.yamlEditor.setValue(this.value)
      }
    }
  },
  mounted() {
    this.yamlEditor = CodeMirror.fromTextArea(this.$refs.textarea, {
      lineNumbers: true, // display line number
      mode: 'text/x-yaml', // grammar model
      gutters: ['CodeMirror-lint-markers'],  // Syntax checker
      theme: 'monokai', // Editor theme
      lint: true, // Turn on grammar checking
      smartIndent: true
    })

    this.yamlEditor.setValue(this.value)
    this.yamlEditor.on('change', (cm) => {
      this.$emit('changed', cm.getValue())
      this.$emit('input', cm.getValue())
    })
  },
  methods: {
    getValue() {
      return this.yamlEditor.getValue()
    },
    test(value) {
      alert(value)
    }
  }
}
</script>

<style scoped>
.yaml-editor{
  height: 100%;
  position: relative;
}
.yaml-editor >>> .CodeMirror {
  height: auto;
  min-height: 300px;
}
.yaml-editor >>> .CodeMirror-scroll{
  min-height: 300px;
}
.yaml-editor >>> .cm-s-rubyblue span.cm-string {
  color: #F08047;
}
</style>
