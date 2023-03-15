import { defineStore } from 'pinia'

const API_URL = "/api/v1";

export const useEvDataStore = defineStore(
    'evDataStore', {
        state: () => ({
            datapoints: [{"id":451,"speed":200,"state_of_charge":50,"shift_state_id":"D","vehicle_id":"123","timestamp":"2023-01-19T14:25:12.336794","odometer":49923.2,"elevation":130,"shift_state":{"id":"D","name":"Drive"}}],
        
            vehicles: [],
            selected_vehicle: 'all',
            from: null,
            to: null,
            order_asc: true,

            //Pagination variables
            selected_page: 1,
            items_per_page: 50,
            total_pages: 10
        }),
        actions: {
            //
            // Get all the vehicle ids from the API
            async fetchVehicleIds(){
                const rsp_full = await fetch(`${API_URL}/vehicles`);
                this.vehicles = await rsp_full.json();
            },
            //
            // Fetch the vehicle data from the API
            async fetchVehicleDatapoints() {
                let url = [`${API_URL}/vehicle_data`];

                // build the url with all the filtering options
                //
                if(this.selected_vehicle != 'all'){
                    url.push(`/${this.selected_vehicle}`)
                }
                url.push('?');
                if(this.from){
                    url.push(`from_date=${this.from}&`);
                }
                if(this.to){
                    url.push(`to_date=${this.to}&`);
                }
                url.push(`page=${this.selected_page}&`);
                url.push(`size=${this.items_per_page}&`);
                url.push(`order=${this.order_asc ? 'asc' : 'desc'}`);

                // fetch the data
                const rsp_full = await fetch(url.join(''));
                const response = await rsp_full.json();

                // unpack the data
                this.datapoints = response.items;
                this.total_pages = Math.floor(response.total/response.size);
                this.page = response.page;

                console.log(this.datapoints);
            }
        },
    }
)