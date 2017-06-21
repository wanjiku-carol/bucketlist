import { Component, OnInit } from '@angular/core';
import { RestangularModule, Restangular } from 'ngx-restangular';
import { Router } from '@angular/router';
import { ModalModule } from 'ngx-bootstrap/modal';
// import { ModalService } from '../_services/index';

@Component({
    selector: 'app-bucketlist',
    templateUrl: './bucketlist.component.html',
    styleUrls: ['./bucketlist.component.css'],
    // moduleId: module.id,
})
export class BucketlistComponent implements OnInit{
    constructor(private restangular: Restangular,private router: Router,) {
    }
    bucketlists;
    current_bucketlist;
    name;
    edit = false;
    // public reroute = false;
    getBuckelists(){
        let baseUrl = this.restangular.all('bucketlists');
        baseUrl.getList().subscribe(resp => {
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
        let addBucketlists = baseUrl.post({'name':this.name}).subscribe(resp => {
            this.getBuckelists();
            this.name = '';
        });
    }
    editBucketlist(id){
        this.edit = true;
        this.current_bucketlist = this.restangular.one('bucketlists', id);
        this.current_bucketlist.get().subscribe(resp => {
            this.name = resp.name;
        });
        // window.location.reload();
    }
    saveBucketlist(){
        this.current_bucketlist.name = this.name
        let editBucketlists = this.current_bucketlist.put().subscribe(resp => {
            this.getBuckelists();
            this.name = '';
            this.edit = false;
        }, function(err) {
            // console.log(err)

        });;
    }

    logout() {
        localStorage.removeItem('auth_token');
        window.location.reload();
    }


    ngOnInit() {
        this.getBuckelists();
    }

}
