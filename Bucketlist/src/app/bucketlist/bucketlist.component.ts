import { Component, OnInit } from '@angular/core';
import { BucketlistService } from './bucketlists.service';
import { RestangularModule, Restangular } from 'ngx-restangular';

@Component({
    selector: 'app-bucketlist',
    templateUrl: './bucketlist.component.html',
    styleUrls: ['./bucketlist.component.css'],
    // providers: [BucketlistService]
})
// export class BucketlistComponent implements OnInit {
//     private bucketlists;
//     private activeTasks;
//
//     constructor(private bucketlistService: BucketlistService) { }
//
//     getBucketlists(){
//         return this.bucketlistService.get().subscribe(bucketlists => {
//             console.log(bucketlists);
//             this.bucketlists = bucketlists;
//             //   this.activeTasks = this.bucketlists.filter(bucketlist => bucketlist.isDone).length;
//         });
//     }
//
//     ngOnInit() {
//         this.getBucketlists();
//     }
//
// }

export class BucketlistComponent {
      constructor(private restangular: Restangular) {
      }
      bucketlists;

      ngOnInit() {
        // GET http://api.test.local/v1/users/2/accounts
        this.bucketlists = this.restangular.all('bucketlists').getList();

        // debugger;
      }
  }
