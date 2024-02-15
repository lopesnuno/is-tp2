import {Body, Controller, Get, ParseIntPipe, Post, Query} from '@nestjs/common';
import { PlayersService } from './players.service';
import {InsertPlayerDto} from "./dto";

@Controller('players')
export class PlayersController {
    constructor(private service: PlayersService) {}

    @Get()
    async getAll(){
        return this.service.findAll();
    }

    @Post('insertPlayer')
    async insertPlayer(@Body() dto: InsertPlayerDto){
        return this.service.insertPlayer(dto);
    }
}
