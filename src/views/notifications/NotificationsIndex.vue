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
                                        <input type="text" required v-model="password.old_password" class="form-control"
                                            placeholder="Subheader for notifications">
                                    </div>
                                </div>
                                <div class="form-group col-md-6">
                                    <label for="">Title for notifications</label>

                                    <div class="">
                                        <input type="text" required v-model="password.new_password" class="form-control"
                                            placeholder="Title for notifications">
                                    </div>
                                </div>
                            </div>

                            <div class="row">
                                <div class="form-group col-md-12">
                                    <label for="">Description</label>
                                    <textarea class="form-control" height="100"></textarea>
                                </div>
                            </div>

                            <div class="row">
                                <div class="form-group col-md-6">
                                    <label for="">Image Url </label>

                                    <div class="">
                                        <input type="text" required v-model="password.confirm_password"
                                            class="form-control" placeholder="Image URL">
                                    </div>
                                </div>
                                <div class="form-group col-md-6">
                                    <label for="">Add tags </label>
                                    <v-combobox hide-selected multiple persistent-hint small-chips>
                                    </v-combobox>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-12">
                                    <v-select v-model="selectedFruits" :items="fruits" label="Favorite Fruits" chips
                                        multiple>
                                        <template v-slot:prepend-item>
                                            <v-list-item ripple @click="toggle">
                                                <v-list-item-action>
                                                    <v-icon :color="selectedFruits.length > 0 ? 'indigo darken-4' : ''">
                                                        {{ icon }}
                                                    </v-icon>
                                                </v-list-item-action>
                                                <v-list-item-content>
                                                    <v-list-item-title>
                                                        Select All
                                                    </v-list-item-title>
                                                </v-list-item-content>
                                            </v-list-item>
                                            <v-divider class="mt-2"></v-divider>
                                        </template>
                                        <template v-slot:append-item>
                                            <v-divider class="mb-2"></v-divider>
                                            <v-list-item disabled>
                                                <v-list-item-avatar color="grey lighten-3">
                                                    <v-icon>
                                                        mdi-food-apple
                                                    </v-icon>
                                                </v-list-item-avatar>

                                                <v-list-item-content v-if="likesAllFruit">
                                                    <v-list-item-title>
                                                        Holy smokes, someone call the fruit police!
                                                    </v-list-item-title>
                                                </v-list-item-content>

                                                <v-list-item-content v-else-if="likesSomeFruit">
                                                    <v-list-item-title>
                                                        Fruit Count
                                                    </v-list-item-title>
                                                    <v-list-item-subtitle>
                                                        {{ selectedFruits.length }}
                                                    </v-list-item-subtitle>
                                                </v-list-item-content>

                                                <v-list-item-content v-else>
                                                    <v-list-item-title>
                                                        How could you not like fruit?
                                                    </v-list-item-title>
                                                    <v-list-item-subtitle>
                                                        Go ahead, make a selection above!
                                                    </v-list-item-subtitle>
                                                </v-list-item-content>
                                            </v-list-item>
                                        </template>
                                    </v-select>
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
    import DashboardLayout from '@/components/Layouts/DashboardLayout'

    export default {
        name: 'Password',
        components: {
            DashboardLayout,
        },
        data() {
            return {
                password: {
                    old_password: '',
                    new_password: '',
                    confirm_password: '',
                },
                model: ['Vuetify'],
                search: '',
                fruits: [
                    'Apples',
                    'Apricots',
                    'Avocado',
                    'Bananas',
                    'Blueberries',
                    'Blackberries'
                ],
                selectedFruits: [],
            }
        },
        methods: {
            handleSubmit() {
                if (this.password.new_password != this.password.confirm_password) {
                    this.$swal('Password not matched');
                }
            },
            toggle() {
                this.$nextTick(() => {
                    if (this.likesAllFruit) {
                        this.selectedFruits = []
                    } else {
                        this.selectedFruits = this.fruits.slice()
                    }
                })
            },
        },
        mounted() {

        },
        watch: {

        },
        computed: {
            likesAllFruit() {
                return this.selectedFruits.length === this.fruits.length
            },
            likesSomeFruit() {
                return this.selectedFruits.length > 0 && !this.likesAllFruit
            },
            icon() {
                if (this.likesAllFruit) return 'mdi-close-box'
                if (this.likesSomeFruit) return 'mdi-minus-box'
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