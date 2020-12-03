<template>
    <dashboard-layout>
        <div slot="main-content">
            <h2 class="dash-title">Upload Image to S3</h2>
            <section class="recent">
                <form v-on:submit.prevent="handleSubmit">
                    <div class="">
                        <div class="activity-card pad-1">
                            <div class="row">
                                <div class="form-group col-md-6">
                                    <label for="">Image Text</label>
                                    <div>
                                        <input type="text" required v-model="text" class="form-control"
                                            placeholder="Text for Image ">
                                    </div>
                                </div>

                                <div class="form-group col-md-6 ">
                                    <label for="">Upload Image</label>

                                    <v-file-input id="file" ref="file" @change="onFileChanged($event)" required chips
                                        multiple label="File input w/ chips"></v-file-input>
                                </div>
                            </div>

                            <v-dialog v-model="dialog" hide-overlay persistent width="800">
                                <v-card color="primary" dark>
                                    <v-card-text>
                                        Uploading image
                                        <v-progress-linear indeterminate color="white" class="mb-0">
                                        </v-progress-linear>
                                    </v-card-text>
                                </v-card>
                            </v-dialog>
                            <div class="form-group">
                                <button type="submit" class="btn btn-main">Upload</button>
                            </div>
                        </div>
                    </div>
                </form>




                <v-simple-table>
                    <template v-slot:default>
                        <thead>
                            <tr>
                                <th class="text-left">
                                    S.no
                                </th>
                                <th class="text-left">
                                    Image Text
                                </th>
                                <th class="text-left">
                                    Image
                                </th>
                                <th class="text-left">
                                    Image Link
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(item,index) in getImages" :key="index">
                                <td>{{ index +1 }}</td>
                                <td>{{ item.image_text }}</td>
                                <td> <img :src="item.image_absoulte_path" class="img-fluid img-responsive"
                                        style="height:200px"> </td>
                                <td>
                                    <v-btn small dark color="primary" :data-link="item.image_path" v-on:click="copyUrl(index)" :id="`btn-${index}`">
                                        Copy
                                    </v-btn>
                                </td>


                            </tr>
                        </tbody>
                    </template>
                </v-simple-table>



            </section>
        </div>
    </dashboard-layout>

</template>

<script>
    import DashboardLayout from '@/components/Layouts/DashboardLayout'
    import axios from 'axios'
    import {
        mapGetters
    } from 'vuex';
    export default {
        name: 'Password',
        components: {
            DashboardLayout,

        },
        data() {
            return {
                text: '',
                image: null,
                file: null,
                selectedFile: null,
                dialog: false,
            }
        },
        methods: {
            update(file) {
                console.log(file)

            },
            handleFileUpload() {
                // console.log(this.$refs.file)
                // this.file = this.$refs.file.files[0];
            },

            async handleSubmit() {


                let formData = new FormData();
                formData.append('image', this.file);
                formData.append('text', this.text);
                console.log(formData)
                this.dialog = true
                axios.post(`${window.url}/api/image`, formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    })
                    .then(res => {
                        console.log(res)
                        this.text = ''
                        this.file = null
                        this.dialog = false
                        this.$store.dispatch('fetchImages')

                    })
            },
            onButtonClick() {
                this.isSelecting = true
                window.addEventListener('focus', () => {
                    this.isSelecting = false
                }, {
                    once: true
                })

                this.$refs.uploader.click()
            },
            onFileChanged(e) {
                console.log(e[0])
                this.file = e[0]
            },
            copyUrl(index) {
                var Url = document.getElementById(`btn-${index}`);
                var x = document.createElement("INPUT");
                x.setAttribute("type", "text");
                x.setAttribute("value" , Url.dataset.link);
                 x.select()  
                 
                 console.log(x)      
                document.execCommand("copy");
                 this.$alertify.success('Text Copied');
            }

        },
        mounted() {
            this.$store.dispatch('fetchImages')
        },
        watch: {
            dialog(val) {
                if (!val) return

                setTimeout(() => (this.dialog = false), 4000)
            },
        },

        computed: mapGetters(['getImages']),

    }
</script>

<style lang="css">
    .pad-1 {
        padding: 1rem
    }
</style>