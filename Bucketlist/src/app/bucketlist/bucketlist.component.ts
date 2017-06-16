import { Component, OnInit } from '@angular/core';
import { BucketlistService } from './bucketlists.service';
import { RestangularModule, Restangular } from 'ngx-restangular';

@Component({
    selector: 'app-bucketlist',
    templateUrl: './bucketlist.component.html',
    styleUrls: ['./bucketlist.component.css'],
})
export class BucketlistComponent implements OnInit{
    constructor(private restangular: Restangular) {
    }
    bucketlists;
    name;
    getBuckelist(){
        let baseUrl = this.restangular.all('bucketlists');
        let getBucketlists = baseUrl.getList().subscribe(resp => {
            this.bucketlists = resp;
        });
    }
    deleteBucketlist(id){
        let baseUrl = this.restangular.one('bucketlists', id);
        let deleteBucketlists = baseUrl.remove().subscribe(resp=>{
            console.log(resp)
            window.location.reload();
        });
    }
    addBucketlist(){
        let baseUrl = this.restangular.all('bucketlists');
        let addBucketlists = baseUrl.post({'name':this.name});
        window.location.reload();
    }
    logout() {
        localStorage.removeItem('auth_token');
        window.location.reload();
    }


    ngOnInit() {
        this.getBuckelist();
    }

}
