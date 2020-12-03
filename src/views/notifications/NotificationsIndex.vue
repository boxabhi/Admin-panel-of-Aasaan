<template>
    <dashboard-layout>
        <div slot="main-content">
        
            <h2 class="dash-title">Send notifications to users</h2>
            
            <section class="recent">
                <form v-on:submit.prevent="handleSubmit">
                    <div class="">
                        <div class="activity-card pad-1">
                            <div class="row">
                                <div class="form-group col-md-6">
                                    <label for="">Subheader for notifications</label>
                                    <div>
                                        <input type="text" required v-model="data.subheader" class="form-control"
                                            placeholder="Subheader for notifications">
                                    </div>
                                </div>
                                <div class="form-group col-md-6">
                                    <label for="">Title for notifications</label>

                                    <div class="">
                                        <input type="text" required v-model="data.title" class="form-control"
                                            placeholder="Title for notifications">
                                    </div>
                                </div>
                            </div>

                            <div class="row">
                                <div class="form-group col-md-12">
                                    <label for="">Description</label>
                                    <textarea class="form-control"  v-model="data.description" height="100"></textarea>
                                </div>
                            </div>

                            <div class="row">
                                <div class="form-group col-md-6">
                                    <label for="">Image Url </label>

                                    <div class="">
                                        <input type="text" required v-model="data.image_url"
                                            class="form-control" placeholder="Image URL">
                                    </div>
                                </div>
                                <div class="form-group col-md-6">
                                    <label for="">Add tags </label>
                                    <v-combobox hide-selected multiple persistent-hint small-chips v-model="data.tag">
                                    </v-combobox>
                                </div>
                            </div>
                            <div class="row">
                                <div class="form-group col-md-12">
                                    <label for="">Mobile for notifications</label>

                                    <div class="">
                                        <input type="text" required v-model="mobiles" class="form-control"
                                            placeholder="Enter mobiles by , separated ">
                                    </div>
                                </div>
                            </div>



                            <div class="form-group col-md-6">
                                <button type="submit" class="btn btn-main">Send notifications <v-icon dark small>mdi-bell</v-icon></button>
                            </div>
                        </div>
                    </div>
                </form>

            </section>
        </div>
    </dashboard-layout>

</template>

<script>
import axios from 'axios'
    import DashboardLayout from '@/components/Layouts/DashboardLayout'
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
                data: {
                    subheader: '',
                    title: '',
                    description: '',
                    image_url : '',
                    tag : '',
                    mobiles : '',
                },
                model: ['Vuetify'],
                search: '',
                mobiles: [],
                selectedMobiles: [],
                
            }
        },
        methods: {
            handleSubmit() {
                var user_mobiles = this.mobiles.split(',')
                var payload = {}
                 payload.user_mobiles = user_mobiles
                 payload.data = this.data
                 axios.post(`${window.url}/send-user-notifications`,payload)
                 .then(res =>{ 
                     console.log(res)
                      this.$swal.fire({
                            icon: 'success',
                            title: 'Success',
                            text: 'Notification send',
                        })
                    this.data = {subheader: '',title: '',description: '',image_url : '',tag : ''}
                    this.selectedMobiles = []
                 })


            },
            toggle() {
                this.$nextTick(() => {
                    if (this.likesAllMobile) {
                        this.selectedMobiles = []
                    } else {
                        this.selectedMobiles = this.mobiles.slice()
                    }
                })
            },
        },
        mounted() {
                this.$store.dispatch('fetchMobiles')
        },
        watch: {

        },
        computed: {
            ...mapGetters(['getMobileNumbers']),
            likesAllMobile() {
                return this.selectedMobiles.length === this.mobiles.length
            },
            likesSomeMobile() {
                return this.selectedMobiles.length > 0 && !this.likesAllMobiles
            },
            icon() {
                if (this.likesAllMobile) return 'mdi-close-box'
                if (this.likesSomeMobile) return 'mdi-minus-box'
                return 'mdi-checkbox-blank-outline'
            },
        },

    }
</script>

<style lang="css">
    .pad-1 {
        padding: 1rem
    }
</style>