<template>
    <div>


        <input type="checkbox" id="sidebar-toggle">
        <div class="sidebar">
            <v-navigation-drawer class="deep-purple accent-4" dark permanent style="background : #027581 !important">
                <h3 class="brand mt-5 pt-5 text-center">
                    <span class="ti-bolt"></span>
                    <span>Aasaan</span>
                </h3>
                <v-list>
                    <v-list-item v-for="item in items" :key="item.title" link>

                        <v-list-item-icon>
                            <v-icon>{{ item.icon }}</v-icon>
                        </v-list-item-icon>
                        <router-link :to="`/${item.link}`">
                            <v-list-item-content>
                                <v-list-item-title class="text-white" style="color:#fff !important">{{ item.title }}
                                </v-list-item-title>
                            </v-list-item-content>
                        </router-link>
                    </v-list-item>
                </v-list>

    <div class="container ml-5">
        <router-link to="/">
        <v-btn color="green" class="ml-5">Logout</v-btn>
        </router-link>
    </div>
            </v-navigation-drawer>
        
        </div>


        <div class="main-content">

            <header>
                <div class="search-wrapper">
                    <span class="ti-search"></span>
                    <input type="search" placeholder="Search">
                </div>

                <div class="social-icons">
                    <span @click="signout" class="ti-power-off"></span>
                    <div></div>
                </div>
            </header>

            <main>
                <slot name="main-content"></slot>
            </main>

        </div>
    </div>
</template>

<script>
    export default {
        name: 'DashboardLayout',
        data() {
            return {
                items: [
                    {
                        title: 'Dashboard',
                        icon: 'mdi-view-dashboard',
                        link: 'dashboard'
                    },
                    {
                        title: 'Super',
                        icon: 'mdi-flower',
                        link: 'super'
                    },

                     {
                        title: 'Question',
                        icon: 'mdi-comment-question-outline',
                        link: 'question'
                    },
                    {
                        title: 'Category',
                        icon: ' mdi-clipboard-outline',
                        link: 'category'
                    },
                    {
                        title: 'Admins',
                        icon: 'mdi-account-settings',
                        link: 'admin/create'
                    },
                      {
                        title: 'Password',
                        icon: 'mdi-key',
                        link: 'password'
                    },
                    
                   

                ],
            }
        },
        methods: {
            signout() {
                localStorage.removeItem('authtoken')
                localStorage.removeItem('admin')
                this.$router.push('/admin/login');
            }
        }
    }
</script>