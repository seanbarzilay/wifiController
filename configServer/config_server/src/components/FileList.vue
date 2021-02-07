<template>
    <div class="file-list">
        <div class="md-layout md-alignment-center">
            <span class="md-headline">Configuration Files</span>
        </div>
        <div class="md-layout md-alignment-center">
            <md-list>
                <md-list-item v-for="file in fileList" :key="file" :to="{path: `/file/${file}`}" exact>
                    {{file}}
                </md-list-item>
            </md-list>
        </div>
        <div class="md-layout md-alignment-center">
            <md-field>
                <label>File Name</label>
                <md-input v-model="fileName"></md-input>
                <span class="md-helper-text">New File ie. conf.yaml</span>
            </md-field>
            <md-button class="md-raised md-primary" v-on:click="newFile()">Create New File</md-button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'config',
        data() {
            return {
                fileList: [],
                fileName: '',
                devices: []
            }
        },
        methods: {
            getFileList() {
                const path = 'http://localhost:5000/config';
                axios.get(path)
                    .then((res) => {
                        this.fileList = res.data.files
                    })
                    .catch((error) => {
                        console.error(error)
                    });
            },
            newFile() {
                this.$router.push('/file/' + this.fileName)
            }
        },
        created() {
            this.getFileList();
        }
    }
</script>
