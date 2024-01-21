import { Controller, Get } from '@nestjs/common';
import { CollegesService } from './colleges.service';

@Controller('colleges')
export class CollegesController {
    constructor(private service: CollegesService) {}

    @Get()
    getAll(){
      return this.service.findAll();
    }
}