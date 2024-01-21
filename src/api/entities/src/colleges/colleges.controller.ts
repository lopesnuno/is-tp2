import {Controller, Get, ParseIntPipe, Query} from '@nestjs/common';
import { CollegesService } from './colleges.service';

@Controller('colleges')
export class CollegesController {
    constructor(private service: CollegesService) {}

    @Get()
    async getAll(){
        return this.service.findAll();
    }
}
