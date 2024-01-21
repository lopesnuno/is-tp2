import {Controller, Get, ParseIntPipe, Query} from '@nestjs/common';
import { PlayersService } from './players.service';

@Controller('players')
export class PlayersController {
    constructor(private service: PlayersService) {}

    @Get()
    async getAll(){
        return this.service.findAll();
    }
}
