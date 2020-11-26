<template>
    <dashboard-layout>
  <div slot="main-content">
     
    <v-container>
      <v-row dense>
        <v-col cols="12">
          <v-card
            color="#385F73"
            dark
          >
            <v-card-title class="headline">
              Welcome to admin Panel of Aasaan
            </v-card-title>

            <v-card-subtitle class="mt-4">Lorem ipsum dolor sit amet consectetur adipisicing elit. Odio adipisci ad harum ex accusamus sint eos praesentium eum, quisquam minima! Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ullam quae esse, voluptas velit nihil ad sed dolor amet fugit corrupti quo deleniti pariatur quos maiores odit maxime optio, voluptates temporibus vitae et! Fugit aliquid, quidem vitae quod quisquam quibusdam deserunt dignissimos odit vero praesentium, error nostrum sed blanditiis voluptates quis voluptas inventore veniam exercitationem vel possimus consectetur velit est? Eum quis odit qui id? Blanditiis minima eaque optio aperiam quam aspernatur, eum error magnam tenetur nam unde nesciunt vitae nulla dignissimos voluptas facere cupiditate! Non, architecto ut ipsa minus expedita magni eveniet mollitia voluptate adipisci quisquam modi! Eius, minima magnam.</v-card-subtitle>

            <v-card-actions>
              <v-btn text>
                Listen Now
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>

      </v-row>
    </v-container>
                    
  </div>
    </dashboard-layout>
</template>
<script>
import DashboardLayout from '@/components/Layouts/DashboardLayout'
    export default {
        data: () => ({
            loading: false,
            selection: 1,
        }),
         components: {
            DashboardLayout,
        },

        methods: {
            reserve() {
                this.loading = true

                setTimeout(() => (this.loading = false), 2000)
            },
        },
    }
</script>